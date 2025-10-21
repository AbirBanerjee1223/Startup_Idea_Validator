"""
Main application module for the Startup Idea Validator.
"""
import os
import logging
import json
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
            tuple: (master_report_dict, pdf_file_path)
        """
        logger.info(f"Starting validation for idea: {startup_idea[:50]}...")

        def run_and_parse(agent, input_text):
            """Helper to run an agent and parse its JSON output."""
            try:
                response_str = agent.run(input_text)
                # Clean the response string before parsing
                # LLMs can sometimes wrap JSON in ```json ... ```
                if response_str.strip().startswith("```json"):
                    response_str = response_str.strip()[7:-3].strip()
                return json.loads(response_str)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON from {agent.name}: {e}")
                logger.error(f"Raw response was: {response_str}")
                return {"error": f"Agent {agent.name} returned invalid JSON.", "raw_response": response_str}
            except Exception as e:
                logger.error(f"An unexpected error occurred with agent {agent.name}: {e}")
                return {"error": f"An unexpected error occurred with agent {agent.name}."}


        # Step 1: Analyze the idea
        logger.info("Step 1: Analyzing idea with Idea Analyst...")
        idea_analysis = run_and_parse(self.idea_analyst, startup_idea)
        
        # Step 2: Research the market
        logger.info("Step 2: Researching market with Market Researcher...")
        market_research = run_and_parse(self.market_researcher, json.dumps(idea_analysis))
        
        # Step 3: Develop business strategy
        logger.info("Step 3: Developing strategy with Business Strategist...")
        strategy_input = {"idea": idea_analysis, "market": market_research}
        business_strategy = run_and_parse(self.business_strategist, json.dumps(strategy_input))
        
        # Step 4: Create financial model
        logger.info("Step 4: Creating financial model with Financial Modeler...")
        financial_input = {"idea": idea_analysis, "market": market_research, "strategy": business_strategy}
        financial_model = run_and_parse(self.financial_modeler, json.dumps(financial_input))
        
        # Step 5: Assess risks
        logger.info("Step 5: Assessing risks with Risk Assessor...")
        risk_input = {"idea": idea_analysis, "market": market_research, "strategy": business_strategy, "financials": financial_model}
        risk_assessment = run_and_parse(self.risk_assessor, json.dumps(risk_input))
        
        # Step 6: Generate final report (pass Python dicts, not JSON strings)
        logger.info("Step 6: Generating final report with Report Generator...")
        master_report_dict, report_path = self.report_generator.generate_report(
            startup_idea, idea_analysis, market_research, 
            business_strategy, financial_model, risk_assessment
        )
        logger.info(f"Report generation complete. Report saved to: {report_path}")
        
        return master_report_dict, report_path


def validate_startup_idea(idea_text):
    """
    Convenience function to validate a startup idea.
    
    Args:
        idea_text (str): The startup idea to validate
        
    Returns:
        tuple: (master_report_dict, pdf_file_path)
    """
    validator = StartupIdeaValidator()
    return validator.validate_idea(idea_text)


if __name__ == "__main__":
    # Example usage
    sample_idea = """
    An AI-powered mobile app called "ReWardrobe" that helps users resell their used clothing. 
    Users take a photo of an item, and the AI will instantly identify it, suggest a fair market price, and auto-generate a title and description. 
    It will also cross-list the item on multiple marketplaces at once, like Poshmark, Depop, and eBay. 
    The app will charge a 5% commission on successful sales.
    """
    
    report, pdf_path = validate_startup_idea(sample_idea)
    print(f"\nReport generated successfully! PDF saved to: {pdf_path}")
    print("\nReport preview:\n")
    print(json.dumps(report, indent=2))
