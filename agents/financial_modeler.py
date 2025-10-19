"""
Financial Modeler Agent for the Startup Idea Validator.
"""
from . import BaseAgent
from utils.prompts import FINANCIAL_MODELER_PROMPT


class FinancialModeler(BaseAgent):
    """
    Agent responsible for suggesting monetization models and possible 
    funding strategies for the startup idea.
    """
    
    def __init__(self):
        super().__init__(
            name="Financial Modeler",
            role_description="Suggests monetization models and funding strategies",
            prompt_template=FINANCIAL_MODELER_PROMPT
        )

    def create_financial_model(self, idea_analysis, market_research, business_strategy):
        """
        Create financial models and monetization strategies based on previous analyses.
        
        Args:
            idea_analysis (str): The analyzed startup idea
            market_research (str): Market research findings
            business_strategy (str): Business strategy including SWOT
            
        Returns:
            str: Financial model and monetization strategies
        """
        combined_input = (
            f"IDEA ANALYSIS:\n{idea_analysis}\n\n"
            f"MARKET RESEARCH:\n{market_research}\n\n"
            f"BUSINESS STRATEGY:\n{business_strategy}"
        )
        return self.run(combined_input)