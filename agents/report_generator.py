"""
Report Generator Agent for the Startup Idea Validator.
"""
from . import BaseAgent
from utils.prompts import REPORT_GENERATOR_PROMPT
from utils.pdf_generator import create_pdf_report


class ReportGenerator(BaseAgent):
    """
    Agent responsible for compiling all findings into a concise evaluation report.
    """
    
    def __init__(self):
        super().__init__(
            name="Report Generator",
            role_description="Compiles all findings into a concise evaluation report",
            prompt_template=REPORT_GENERATOR_PROMPT
        )

    def generate_report(self, startup_idea, idea_analysis, market_research, 
                        business_strategy, financial_model, risk_assessment):
        """
        Generate a comprehensive report based on all analyses.
        
        Args:
            startup_idea (str): The original startup idea
            idea_analysis (str): The analyzed startup idea
            market_research (str): Market research findings
            business_strategy (str): Business strategy including SWOT
            financial_model (str): Financial model and monetization strategies
            risk_assessment (str): Risk assessment report
            
        Returns:
            tuple: (report_content, report_file_path)
        """
        combined_input = (
            f"ORIGINAL STARTUP IDEA:\n{startup_idea}\n\n"
            f"IDEA ANALYSIS:\n{idea_analysis}\n\n"
            f"MARKET RESEARCH:\n{market_research}\n\n"
            f"BUSINESS STRATEGY:\n{business_strategy}\n\n"
            f"FINANCIAL MODEL:\n{financial_model}\n\n"
            f"RISK ASSESSMENT:\n{risk_assessment}"
        )
        
        # Generate the consolidated report
        report_content = self.run(combined_input)
        
        # Create PDF file
        report_file_path = create_pdf_report(startup_idea, report_content)
        
        return report_content, report_file_path