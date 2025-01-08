from openai import OpenAI
import os
from typing import Type, TypeVar
from pydantic import BaseModel
from openai import OpenAI

T = TypeVar("T", bound=BaseModel)

# Chunking strategy that avoids chunking mid-sentence and partial tables
def split_into_chunks(text: str, max_chunk_size: int) -> list[str]:
    """
    Splits the input text into chunks of a specified maximum size.
    Ensures that chunks do not split tables or sentences.
    """
    lines = text.splitlines()
    chunks = []
    current_chunk = []

    for line in lines:
        # Check if adding this line exceeds the chunk size
        if sum(len(l) for l in current_chunk) + len(line) + len(current_chunk) < max_chunk_size:
            current_chunk.append(line)
        else:
            # Ensure no partial table chunks
            if line.startswith("|") or (current_chunk and current_chunk[-1].startswith("|")):
                # Complete the current table before starting a new chunk
                current_chunk.append(line)
            else:
                chunks.append("\n".join(current_chunk))
                current_chunk = [line]
    if current_chunk:
        chunks.append("\n".join(current_chunk))
    return chunks

def extract_with_llm(chunk: str, schema: Type[T]) -> T:
    """
    Extracts structured data from a text chunk using the LLM and a Pydantic model schema.
    """
    prompt = f"""
    Extract the HVAC part data from the following text and structure it according to the provided model.

    Special Instructions:
        - Emerson Climate Technologies is now called Copeland. Please use the new brand name.

    Text:
    {chunk}
    """

    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

    response = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output structured data."},
            {"role": "user", "content": prompt}
        ],
        response_format=schema,  # Pass the Pydantic model directly
    )

    return response.choices[0].message.parsed  # This will be a Pydantic model instance

def merge_results(results: list[T], schema: Type[T]) -> T:
    """
    Merges multiple Pydantic model instances into a single instance.
    """
    merged_data = {}
    for result in results:
        for field, value in result.model_dump().items():
            if value is not None:  # Prioritize non-None values
                merged_data[field] = value
    return schema.model_validate(merged_data)

def extract_data_from_markdown(content: str, schema: Type[T], max_chunk_size: int = 3000) -> T:
    """
    Extracts structured data from long markdown content using chunking and LLM extraction.
    """
    chunks = split_into_chunks(content, max_chunk_size)
    partial_results = [extract_with_llm(chunk, schema) for chunk in chunks]
    return merge_results(partial_results, schema)

def extract_data_from_multiple_sources(
    contents: list[str],
    schema: Type[T],
    max_chunk_size: int = 3000
) -> T:
    """
    Extracts structured data from multiple markdown contents.
    
    Args:
        contents: List of markdown strings.
        schema: Pydantic model schema for the output.
        max_chunk_size: Maximum size of each chunk.
        
    Returns:
        A merged Pydantic model instance with data from all contents.
    """
    all_partial_results = []

    for content in contents:
        # Split each content into chunks
        chunks = split_into_chunks(content, max_chunk_size)
        # Extract data from each chunk
        partial_results = [extract_with_llm(chunk, schema) for chunk in chunks]
        all_partial_results.extend(partial_results)

    # Merge results from all documents
    return merge_results(all_partial_results, schema)