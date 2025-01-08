import requests
import tempfile
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader
import nest_asyncio
from bs4 import BeautifulSoup

# Enable async operations
nest_asyncio.apply()

# Parse HTML and extract PDF links
def extract_pdf_links(html_content, desired_link_texts):
  """
  Extracts PDF links from HTML content based on a list of desired link texts.

  Args:
      html_content (str): The HTML content of the page.
      desired_link_texts (list of str): A list of link texts to search for.

  Returns:
      dict: A dictionary mapping each desired link text to its corresponding URL.
            If a link is not found, its value will be None.
  """

  soup = BeautifulSoup(html_content, 'html.parser')
  pdf_links = {text.lower(): None for text in desired_link_texts}

  # Case-insensitive matching
  normalized_texts = {text.lower(): text for text in desired_link_texts}

  # Iterate over all <a> tags with href attribute
  for a_tag in soup.find_all('a', href=True):
      link_text = a_tag.get_text(strip=True).lower()
      for key in pdf_links.keys():
          if key == link_text:
              # Assign the href to the corresponding original text key
              pdf_links[normalized_texts[key]] = a_tag['href']

  return pdf_links

def parse_pdf_from_url(pdf_url):
    """
    Download a PDF from a URL, process it with LlamaParse, and return the parsed content.

    Args:
        pdf_url (str): The URL of the PDF to download.

    Returns:
        list: Parsed documents from the PDF.
    """
    # Create a temporary file to store the downloaded PDF
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=True) as temp_pdf:
        # Download the PDF
        response = requests.get(pdf_url)
        if response.status_code != 200:
            raise ValueError(f"Failed to download PDF. Status code: {response.status_code}")
        temp_pdf.write(response.content)
        temp_pdf.flush()  # Ensure all data is written

        # Set up the LlamaParse parser with quiet mode
        parser = LlamaParse(
            result_type="markdown",
            verbose=False  # Disable default logging
        )
        file_extractor = {".pdf": parser}

        # Parse the downloaded PDF using SimpleDirectoryReader
        documents = SimpleDirectoryReader(
            input_files=[temp_pdf.name], 
            file_extractor=file_extractor
        ).load_data()

    return documents