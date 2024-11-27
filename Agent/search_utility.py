import logging
from duckduckgo_search import DDGS
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class TravelSearchUtility:
    def __init__(self):
        self.ddgs = DDGS()
        
    def search_travel_info(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """
        Search for travel-related information using DuckDuckGo.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return (default: 5)
            
        Returns:
            List of dictionaries containing search results with 'title', 'link', and 'snippet' keys
        """
        try:
            # Add travel-specific keywords to improve search relevance
            travel_query = f"travel {query} guide information tourism"
            
            # Perform the search
            results = []
            for r in self.ddgs.text(travel_query, max_results=max_results):
                results.append({
                    'title': r['title'],
                    'link': r['link'],
                    'snippet': r['body']
                })
            
            return results
        except Exception as e:
            logger.error(f"Error searching DuckDuckGo: {str(e)}")
            return []
    
    def get_destination_highlights(self, destination: str) -> Optional[Dict[str, List[str]]]:
        """
        Get key highlights about a travel destination.
        
        Args:
            destination: Name of the destination
            
        Returns:
            Dictionary containing categorized highlights or None if error occurs
        """
        try:
            highlights = {
                'attractions': [],
                'activities': [],
                'food': [],
                'culture': []
            }
            
            # Search for attractions
            attractions = self.ddgs.text(
                f"{destination} top tourist attractions must see",
                max_results=3
            )
            highlights['attractions'] = [r['title'] for r in attractions]
            
            # Search for activities
            activities = self.ddgs.text(
                f"{destination} best things to do activities",
                max_results=3
            )
            highlights['activities'] = [r['title'] for r in activities]
            
            # Search for food
            food = self.ddgs.text(
                f"{destination} traditional food cuisine must try",
                max_results=3
            )
            highlights['food'] = [r['title'] for r in food]
            
            # Search for culture
            culture = self.ddgs.text(
                f"{destination} culture customs traditions",
                max_results=3
            )
            highlights['culture'] = [r['title'] for r in culture]
            
            return highlights
            
        except Exception as e:
            logger.error(f"Error getting destination highlights: {str(e)}")
            return None
    
    def get_travel_tips(self, destination: str, category: str = 'general') -> List[str]:
        """
        Get travel tips for a specific destination and category.
        
        Args:
            destination: Name of the destination
            category: Type of tips (e.g., 'safety', 'budget', 'weather', 'transport', 'general')
            
        Returns:
            List of travel tips
        """
        try:
            query = f"{destination} travel tips {category} advice"
            results = self.ddgs.text(query, max_results=5)
            
            tips = []
            for r in results:
                # Extract relevant information from the snippet
                snippet = r['body']
                if len(snippet) > 30:  # Only include substantial tips
                    tips.append(snippet)
            
            return tips
        except Exception as e:
            logger.error(f"Error getting travel tips: {str(e)}")
            return []
