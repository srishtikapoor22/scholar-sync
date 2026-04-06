from langchain_core.tools import tool
from tavily import TavilyClient
import os
from dotenv import load_dotenv
load_dotenv()

tavily=TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query:str)->str:
    '''Search the web for the latest 2026 status of a technical library, hardware, or API. Use this to find if something is outdated, deprecated, or has a 2026 successor.'''
    response=tavily.search(query=query,search_depth="advanced",max_results=3)
    search_results=[
        f"Source: {res['url']}\nContent: {res['content']}"
        for res in response["results"]
     ]
    return "\n\n".join(search_results)