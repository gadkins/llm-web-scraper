from dotenv import load_dotenv
import os
from firecrawl import FirecrawlApp

load_dotenv()

FIRECRAWL_API_KEY = os.getenv('FIRECRAWL_API_KEY')
app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

 # Map a site
def map_url(url, search_term=None) -> list[str]:
  """
  Map a site with optional search term
  Returns a list of links
  """
  map_result = app.map_url(
    url,
    params={
        'search': search_term
    })
  return map_result['links']

 # Crawl url
def crawl_url(url, limit=20, allow_backward_links=True, formats=["markdown", "html"], poll_interval=30):
  data = app.crawl_url(
    url,
    params={
    'limit': limit,
    "allowBackwardLinks": allow_backward_links,
    'scrapeOptions': {'formats': formats}
    },
    poll_interval=poll_interval
  )
  return data

# Scrape url
def basic_scrape(url, formats=["markdown", "html"]):
  return app.scrape_url(
      url,
      params={'formats': formats})

# LLM extract
def advanced_scrape(url, schema, system_prompt=''):
  data = app.scrape_url(
    url, {
    'formats': ['extract'],
    'extract': {
        'schema': schema.model_json_schema(),
        'systemPrompt': system_prompt
    }
  })
