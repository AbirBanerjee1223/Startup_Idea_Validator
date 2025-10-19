"""
Risk Assessor Agent for the Startup Idea Validator.
"""
from . import BaseAgent
from utils.prompts import RISK_ASSESSOR_PROMPT


class RiskAssessor(BaseAgent):
    """
    Agent responsible for highlighting potential technical, legal, and market risks
    for the startup idea.
    """
    
    def __init__(self):
        super().__init__(
            name="Risk Assessor",
            role_description="Highlights potential technical, legal, and market risks",
            prompt_template=RISK_ASSESSOR_PROMPT
        )

    def assess_risks(self, idea_analysis, market_research, business_strategy, financial_model):
        """
        Assess risks associated with the startup idea based on all previous analyses.
        
        Args:
            idea_analysis (str): The analyzed startup idea
            market_research (str): Market research findings
            business_strategy (str): Business strategy including SWOT
            financial_model (str): Financial model and monetization strategies
            
        Returns:
            str: Risk assessment report
        """
        combined_input = (
            f"IDEA ANALYSIS:\n{idea_analysis}\n\n"
            f"MARKET RESEARCH:\n{market_research}\n\n"
            f"BUSINESS STRATEGY:\n{business_strategy}\n\n"
            f"FINANCIAL MODEL:\n{financial_model}"
        )
        return self.run(combined_input)