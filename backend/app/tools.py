from langchain_core.tools import tool
from tavily import TavilyClient
import os
from dotenv import load_dotenv

# Load environment variables from project root
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
load_dotenv(os.path.join(project_root, '.env'))

tavily=TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query:str, is_time_sensitive: bool)->str:
    '''Search the web for the latest 2026 status of a technical library, hardware, or API. Use this to find if something is outdated, deprecated, or has a 2026 successor.
    is_time_sensitive: Set to True for versions/hardware, False for math/foundations.'''
    print(f"DEBUG: web_search called with query: {query}")
    try:
        response=tavily.search(query=query,search_depth="advanced",max_results=3)
        print(f"DEBUG: Tavily response received: {len(response.get('results', []))} results")
        search_results=[
            f"Source: {res['url']}\nContent: {res['content']}"
            for res in response["results"]
         ]
        return "\n\n".join(search_results)
    except Exception as e:
        print(f"DEBUG: Tavily search failed: {e}")
        return f"Search failed: {e}"