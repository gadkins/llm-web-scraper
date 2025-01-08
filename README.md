# Web Scraper

This tool can be used to scrape HVAC catalog components from a website and save the data to a spreadsheet. This tool is experimental and has only been partially tested on [bakerdist.com](https://www.bakerdist.com/). It currently takes about 30 seconds to scrape and process a single component.

## Status

- [x] Map a site to find all URLs
- [x] Filter URLs by a search term (e.g. "compressor")
- [x] Add support for custom schemas to enforce structure of LLM response
- [x] Scrape a list of URLs
- [x] Save scraped data to a `.csv` and `.xlsx` files
- [ ] Save intermediate data to file (currently only saved when the process completes)
- [ ] Add ability to checkpoint and resume
- [ ] Add ability to scrape multiple URLs in parallel

## Prerequisites

- [Firecrawl API key](https://www.firecrawl.dev/app/api-keys) (For crawling and scraping)
- [LlamaCloud API key](https://cloud.llamaindex.ai/) (For parsing PDF files)
- [OpenAI API key](https://platform.openai.com/api-keys) (For LLM extraction)

## Example Usage

```bash
python main.py --url https://www.bakerdist.com/ \
--search compressor \
--schema models.compressor.CompressorSpec \
--pdf-link-text "specification sheet" \
--limit 10
```

Available options:

```bash
--url: The URL to scrape (required)
--search: The search term to filter URLs by (optional, default is "compressor")
--schema: The import path to the schema class (optional, default is "models.compressor.CompressorSpec")
--pdf-link-text: A list of PDF links to extract (i.e. the `<a>` tag text) (optional, default is "specification sheet")
--limit: The number of URLs to scrape (optional, default is all links returned by `map_urls`)
--output: The output file name (optional, defaults is "output.csv" and "output.xlsx")
--append: Append output to an existing file (optional, default is False). Otherwise, it will overwrite the output file.
```

To use a custom schema, you must create a new file in the [`models`](./models/) directory.

## Setup

1. Change to the `scripts/web-scraper` directory.

    ```bash
    cd scripts/web-scraper
    ```

2. Set the following environment variables in a `.env` file:

    ```
    FIRECRAWL_API_KEY=
    LLAMACLOUD_API_KEY=
    OPENAI_API_KEY=
    ```

3. Create and activate a virtual environment:

    ```bash
    python -m venv .venv 
    source .venv/bin/activate
    ```

4. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Create a new schema class in the [`models`](./models/) directory that corresponds to the catalog component you are scraping.

    This is a Pydantic model that defines the desired structure of the LLM response.

    **Be sure to update the `field_mapping` in [`main.py`](./main.py) to match the fields in your schema so that the data can be saved to an Excel/CSV file with corresponding column headers.**

6. Run the script:

    ```bash
    python main.py --url https://www.bakerdist.com/ \
      --search compressor \
      --limit 10 \
      --output output.csv \
      --append
    ```
