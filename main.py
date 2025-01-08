import argparse
from scrapers.firecrawl import map_url, basic_scrape
from extractors.pdf import extract_pdf_links, parse_pdf_from_url
from extractors.llm import extract_data_from_multiple_sources
from models.compressor import CompressorSpec
from utils.excel import save_to_spreadsheet, add_rows_to_excel, parse_model_to_filtered_dict
import os
from tqdm import tqdm
from importlib import import_module

def process_single_url(url: str, desired_pdf_links: list[str], schema_path: str):
    """
    Process a single URL and extract structured data
    
    Args:
        url: The URL to process
        desired_pdf_links: List of PDF link texts to look for
        schema_path: Import path to the schema class (e.g., 'models.compressor.CompressorSpec')
    """
    # Import the schema dynamically
    module_path, class_name = schema_path.rsplit('.', 1)
    module = import_module(module_path)
    schema_class = getattr(module, class_name)
    
    tqdm.write(f"Starting to process URL: {url}")
    main_content = basic_scrape(url)
    tqdm.write(f"Basic scrape completed. Content length: {len(main_content.get('markdown', ''))}")
    
    source_url = main_content['metadata']['sourceURL']
    main_content_md = main_content['markdown']

    # Extract and parse PDF
    pdf_links = extract_pdf_links(main_content['html'], desired_pdf_links)
    spec_sheet_content = ""
    
    for link_text, pdf_link in pdf_links.items():
        if pdf_link:
            try:
                parsed_content = parse_pdf_from_url(pdf_link)
                for item in parsed_content:
                    spec_sheet_content += item.text
            except Exception as e:
                print(f"Error processing PDF {link_text}: {str(e)}")

    # Combine contents and extract data
    markdown_contents = [main_content_md, spec_sheet_content]
    result = extract_data_from_multiple_sources(markdown_contents, schema_class)
    
    # Update with source URL
    updated_spec = result.model_copy(update={"link": source_url})
    return updated_spec

def main():
    parser = argparse.ArgumentParser(description='HVAC Part Scraper')
    parser.add_argument('--url', type=str, required=True, help='Root URL to scrape')
    parser.add_argument('--search', type=str, default='compressor', help='Search term')
    parser.add_argument('--pdf-link-text', type=list, default=['specification sheet'], help='PDF link text to extract')
    parser.add_argument('--output', type=str, default='output.xlsx', help='Output Excel file')
    parser.add_argument('--append', action='store_true', help='Append to existing file')
    parser.add_argument('--limit', type=int, help='Maximum number of links to process')
    parser.add_argument(
        '--schema',
        type=str,
        default='models.compressor.CompressorSpec',
        help='Import path to the schema class (e.g., models.compressor.CompressorSpec)'
    )
    
    args = parser.parse_args()

    # Field mapping for Excel output
    field_mapping = {
        "Product Name": "product_name",
        "Type": "compressor_type",
        "Length [in]": "length_in",
        "Width [in]": "width_in",
        "Height [in]": "height_in",
        "Price": "price",
        "Weight [lb]": "weight_lb",
        "Manufacturer": "brand",
        "Model No": "model_no",
        "Tonnage": "tonnage",
        "Displacement Unit": "displacement_unit",
        "Displacement": "displacement",
        "Lower RPM": "lower_rpm",
        "Upper RPM": "upper_rpm",
        "Cycle [Hz]": "cycle_hertz",
        "Refrigerant": "refrigerant",
        "Description": "description",
        "Link": "link",
        "Used In": "used_in"
    }

    # Map URLs
    tqdm.write(f"Searching {args.url} for keyword '{args.search}'...")
    links = map_url(args.url, search_term=args.search)

    if not links:
        tqdm.write("No links found! Exiting...")
        return
    
    # Skip the first 3 links and the last 1
    links = links[3:-1]
    
    # Apply limit if specified
    if args.limit:
        links = links[:args.limit]
        print(f"Processing first {args.limit} links...")

    all_results = []
    # Create progress bar
    progress_bar = tqdm(links, desc="Processing links", total=len(links))
    for link in progress_bar:
        try:
            result = process_single_url(link, args.pdf_link_text, args.schema)
            filtered_data = parse_model_to_filtered_dict(result, field_mapping)
            all_results.append(filtered_data)
        except Exception as e:
            tqdm.write(f"Error processing {link}: {str(e)}")
            continue

    # Get base filename without extension
    base_filename = os.path.splitext(args.output)[0]
    
    # Ensure Excel file has .xlsx extension
    excel_filename = (
        args.output if args.output.endswith('.xlsx') 
        else f"{base_filename}.xlsx"
    )
    csv_filename = f"{base_filename}.csv"

    if args.append and os.path.exists(excel_filename):
        print(f"Appending {len(all_results)} rows to existing file")
        add_rows_to_excel(excel_filename, all_results, field_mapping)
    else:
        save_to_spreadsheet(
            all_results, 
            field_mapping, 
            excel_filename=excel_filename,
            csv_filename=csv_filename
        )

    print(f"Results saved to {excel_filename} and {csv_filename}")

if __name__ == "__main__":
    main() 