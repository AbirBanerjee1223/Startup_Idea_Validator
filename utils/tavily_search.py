"""
Web search utilities using Tavily API for the Startup Idea Validator.
"""
import os
import json
import requests
from typing import List, Dict, Any, Optional

from config import TAVILY_API_KEY

TAVILY_SEARCH_URL = "https://api.tavily.com/search"


def search_web(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Search the web using Tavily API.
    
    Args:
        query (str): Search query
        max_results (int): Maximum number of results to return
        
    Returns:
        List[Dict[str, Any]]: List of search results
    """
    if not TAVILY_API_KEY:
        raise ValueError("Tavily API key not found. Please set TAVILY_API_KEY in .env file.")
    
    # Prepare request
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": TAVILY_API_KEY
    }
    
    data = {
        "query": query,
        "max_results": max_results,
        "search_depth": "advanced",
        "include_answer": True,
        "include_domains": [],
        "exclude_domains": []
    }
    
    # Make request
    response = requests.post(
        TAVILY_SEARCH_URL,
        headers=headers,
        data=json.dumps(data)
    )
    
    if response.status_code != 200:
        raise Exception(f"Tavily API error: {response.status_code} - {response.text}")
    
    results = response.json()
    return results.get("results", [])


def research_startup_domain(
    domain: str, 
    problem: Optional[str] = None, 
    solution: Optional[str] = None
) -> Dict[str, Any]:
    """
    Research a startup domain using Tavily API.
    
    Args:
        domain (str): The industry or domain of the startup
        problem (str, optional): The problem the startup is trying to solve
        solution (str, optional): The solution the startup is offering
        
    Returns:
        Dict[str, Any]: Research results
    """
    # Build search queries
    queries = [
        f"latest trends in {domain} industry",
        f"market size of {domain} industry",
        f"top companies in {domain} industry"
    ]
    
    if problem:
        queries.append(f"companies solving {problem} in {domain}")
    
    if solution:
        queries.append(f"similar solutions to {solution} in {domain}")
    
    # Perform searches
    all_results = {}
    for query in queries:
        try:
            results = search_web(query, max_results=3)
            all_results[query] = results
        except Exception as e:
            all_results[query] = {"error": str(e)}
    
    return all_results


