import asyncio
import json
#import os
#from typing import List
from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from pydantic import BaseModel, Field
import pandas as pd 

# Website URL
website_url = ""


################################################# READ THE COMMENT BELOW ############################################################### 
"""
!!!
Define the instruction for extraction
AND ALSO IF YOU WANT TO EXTRACT DATA FROM A WESBITE WHICH DOES NOT HAVE ENGLISH WRITTEN DATA FOR EXAMPLE: TURKISH THEN TRANSLATE
THE INSTRUCTION AND THE CLASS COMPANYInfo TEXTS TO THAT LANGUAGE SO IN THIS CASE TURKISH. 
THIS WAY THE SYSTEM WORKS A BIT BETTER BASED ON MY TESTS...
!!!!
"""
########################################################################################################################################

INSTRUCTION = """Extract the following fields from the given HTML content and present them in a structured format. The data should include information within anchor tags (e.g., <a href="...">...</a>):

1. Company Name
2. Address
3. Contact (Phone Number) — extract both the displayed number and the number in the href attribute.
4. Website — extract both the displayed URL and the URL in the href attribute.
5. Salon
6. Stand Number

Match the data with the correct fields, and note any missing or incorrect information. Format the extracted data clearly."""

class CompanyInfo(BaseModel):
    company_name: str = Field(description="The name of the company")
    phone_number: str = Field(description="The contact phone number of the company")
    address: str = Field(description="The full address of the company")
    website: str = Field(description="The website of the company")
    hall: str = Field(description="The exhibition hall number")
    stand_number: str = Field(description="The exhibition stand number")


async def main():
    llm_strategy = LLMExtractionStrategy(
        provider="gemini/gemini-1.5-pro",   #Model name based on the API key I have
        api_token="",                       #Add the API key here
        schema=CompanyInfo.model_json_schema(),
        extraction_type="schema",
        instruction=INSTRUCTION,
        chunk_token_threshold = 1000,   
        overlap_rate = 0.0,
        apply_chunking=True,
        input_format="markdown",
        extra_args={"temperature":0.0,"max_tokens":800},
    )

    crawl_config = CrawlerRunConfig(
        extraction_strategy=llm_strategy,
        cache_mode=CacheMode.BYPASS,
        process_iframes=False,
        exclude_external_links=True,
    )

    browser_config = BrowserConfig(headless=True, verbose=True)

    try:
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(url=website_url, config=crawl_config)
            
            if result.success:
                data = json.loads(result.extracted_content)
                print("Extracted items:", data)
                df = pd.DataFrame(data)
                df = df.applymap(lambda x: x.encode('latin1').decode('utf-8') if isinstance(x, str) else x)
                output_file = "extracted_company_info.xlsx"
                df.to_excel(output_file, index=False)
                print(f"Data has been successfully saved to {output_file}")
                
                llm_strategy.show_usage()
            else:
                print("Error:", result.error_message)
                
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())