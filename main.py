"""
Main application module for the Startup Idea Validator.
"""
import logging
import json
from agents.idea_analyst import IdeaAnalyst
from agents.market_researcher import MarketResearcher
from agents.business_strategist import BusinessStrategist
from agents.financial_modeler import FinancialModeler
from agents.risk_assessor import RiskAssessor
from agents.report_generator import ReportGenerator
from utils.pdf_generator import create_pdf_report 
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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
        Run the complete validation process. This is a generator that yields status updates.
        """
        logger.info(f"Starting validation for idea: {startup_idea[:50]}...")

        def run_agent(agent, input_data):
            """Helper function to run an agent and handle data formats."""
            if isinstance(input_data, dict):
                input_str = json.dumps(input_data, indent=2)
            else:
                input_str = input_data
            
            try:
                response_dict = agent.run(input_str)
                return response_dict
            except Exception as e:
                logger.error(f"An error occurred with agent {agent.name}: {e}")
                return {"error": f"An error occurred with agent {agent.name}.", "details": str(e)}

        # Step 1: Analyze the idea
        yield "Analyzing idea..."
        idea_analysis = run_agent(self.idea_analyst, startup_idea)
        
        
        # Step 2: Research the market
        yield "Researching market..."
        market_research = run_agent(self.market_researcher, idea_analysis)
        
        
        # Step 3: Develop business strategy
        yield "Developing strategy..."
        strategy_input = {"idea": idea_analysis, "market": market_research}
        business_strategy = run_agent(self.business_strategist, strategy_input)
        
        
        # Step 4: Create financial model
        yield "Modeling financials..."
        financial_input = {"idea": idea_analysis, "market": market_research, "strategy": business_strategy}
        financial_model = run_agent(self.financial_modeler, financial_input)
        
        
        # Step 5: Assess risks
        yield "Assessing risks..."
        risk_input = {"idea": idea_analysis, "market": market_research, "strategy": business_strategy, "financials": financial_model}
        risk_assessment = run_agent(self.risk_assessor, risk_input)
        
        
        # Step 6: Generate final report summary
        yield "Generating final report..."
        report_input_data = {
            "startup_idea": startup_idea, "idea_overview": idea_analysis, "market_landscape": market_research,
            "business_strategy": business_strategy, "financial_outlook": financial_model, "risk_assessment": risk_assessment
        }
        final_summary_data = run_agent(self.report_generator, report_input_data)

        # Assemble the final master dictionary for the UI
        master_report_dict = {
            "summary_data": final_summary_data,
            "detailed_data": report_input_data
        }
        
        # --- THIS IS THE FIX ---
        # Call the PDF generator with the single master dictionary argument it expects.
        logger.info("Generating PDF report...")
        report_path = create_pdf_report(master_report_dict)
        logger.info(f"Report generation complete. PDF saved to: {report_path}")
        
        # Yield the final tuple for the Streamlit app
        yield master_report_dict, report_path


def validate_startup_idea(idea_text):
    """Convenience function that yields from the validator."""
    validator = StartupIdeaValidator()
    return (yield from validator.validate_idea(idea_text))


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
