"""
Business Strategist Agent for the Startup Idea Validator.
"""
from . import BaseAgent
from utils.prompts import BUSINESS_STRATEGIST_PROMPT


class BusinessStrategist(BaseAgent):
    """
    Agent responsible for conducting SWOT analysis and checking product-market fit
    for the startup idea.
    """
    
    def __init__(self):
        super().__init__(
            name="Business Strategist",
            role_description="Conducts SWOT analysis and checks product-market fit",
            prompt_template=BUSINESS_STRATEGIST_PROMPT
        )

    def develop_strategy(self, idea_analysis, market_research):
        """
        Develop business strategy based on idea analysis and market research.
        
        Args:
            idea_analysis (str): The analyzed startup idea
            market_research (str): Market research findings
            
        Returns:
            str: Business strategy including SWOT analysis
        """
        combined_input = f"IDEA ANALYSIS:\n{idea_analysis}\n\nMARKET RESEARCH:\n{market_research}"
        return self.run(combined_input)