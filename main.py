"""
Main application module for the Startup Idea Validator.
"""
import os
import logging
from datetime import datetime

from agents.idea_analyst import IdeaAnalyst
from agents.market_researcher import MarketResearcher
from agents.business_strategist import BusinessStrategist
from agents.financial_modeler import FinancialModeler
from agents.risk_assessor import RiskAssessor
from agents.report_generator import ReportGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class StartupIdeaValidator:
    """Main orchestrator for the Startup Idea Validator system."""
    
    def __init__(self):
        """Initialize all agents."""
        logger.info("Initializing Startup Idea Validator")
        self.idea_analyst = IdeaAnalyst()
        self.market_researcher = MarketResearcher()
        self.business_strategist = BusinessStrategist()
        self.financial_modeler = FinancialModeler()
        self.risk_assessor = RiskAssessor()
        self.report_generator = ReportGenerator()
    
    def validate_idea(self, startup_idea):
        """
        Run the complete validation process on a startup idea.
        
        Args:
            startup_idea (str): The raw startup idea to validate
            
        Returns:
            tuple: (markdown_report, pdf_file_path)
        """
        logger.info(f"Starting validation for idea: {startup_idea[:50]}...")
        
        # Step 1: Analyze the idea
        logger.info("Step 1: Analyzing idea with Idea Analyst...")
        idea_analysis = self.idea_analyst.analyze_idea(startup_idea)
        logger.info("Idea analysis complete")
        
        # Step 2: Research the market
        logger.info("Step 2: Researching market with Market Researcher...")
        market_research = self.market_researcher.research_market(idea_analysis)
        logger.info("Market research complete")
        
        # Step 3: Develop business strategy
        logger.info("Step 3: Developing strategy with Business Strategist...")
        business_strategy = self.business_strategist.develop_strategy(
            idea_analysis, market_research
        )
        logger.info("Business strategy development complete")
        
        # Step 4: Create financial model
        logger.info("Step 4: Creating financial model with Financial Modeler...")
        financial_model = self.financial_modeler.create_financial_model(
            idea_analysis, market_research, business_strategy
        )
        logger.info("Financial modeling complete")
        
        # Step 5: Assess risks
        logger.info("Step 5: Assessing risks with Risk Assessor...")
        risk_assessment = self.risk_assessor.assess_risks(
            idea_analysis, market_research, business_strategy, financial_model
        )
        logger.info("Risk assessment complete")
        
        # Step 6: Generate final report
        logger.info("Step 6: Generating final report with Report Generator...")
        report_content, report_path = self.report_generator.generate_report(
            startup_idea, idea_analysis, market_research, 
            business_strategy, financial_model, risk_assessment
        )
        logger.info(f"Report generation complete. Report saved to: {report_path}")
        
        return report_content, report_path


def validate_startup_idea(idea_text):
    """
    Convenience function to validate a startup idea.
    
    Args:
        idea_text (str): The startup idea to validate
        
    Returns:
        tuple: (markdown_report, pdf_file_path)
    """
    validator = StartupIdeaValidator()
    return validator.validate_idea(idea_text)


if __name__ == "__main__":
    # Example usage
    sample_idea = """
    A mobile app that connects local farmers directly with consumers, 
    allowing people to buy fresh produce, dairy, and meat directly from 
    nearby farms. The app would show what's in season, handle payments, 
    and coordinate pickup or delivery options.
    """
    
    report, pdf_path = validate_startup_idea(sample_idea)
    print(f"\nReport generated successfully! PDF saved to: {pdf_path}")
    print("\nReport preview:\n")
    print(report[:500] + "...\n")