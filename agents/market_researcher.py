"""
Market Researcher Agent for the Startup Idea Validator.
"""
from . import BaseAgent
from utils.prompts import MARKET_RESEARCHER_PROMPT


class MarketResearcher(BaseAgent):
    """
    Agent responsible for researching the market, including existing competitors,
    market trends, size, and overall viability of the startup idea.
    """
    
    def __init__(self):
        super().__init__(
            name="Market Researcher",
            role_description="Searches for existing competitors, trends, and market viability",
            prompt_template=MARKET_RESEARCHER_PROMPT
        )

    def research_market(self, idea_analysis):
        """
        Research the market based on the analyzed idea.
        
        Args:
            idea_analysis (str): The analyzed startup idea from the Idea Analyst
            
        Returns:
            str: Market research findings
        """
        return self.run(idea_analysis)