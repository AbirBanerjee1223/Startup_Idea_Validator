import json
from . import BaseAgent
from utils.prompts import REPORT_GENERATOR_PROMPT
from utils.pdf_generator import create_pdf_report 

class ReportGenerator(BaseAgent):
    """
    Agent responsible for compiling all findings and generating the final structured report.
    """
    
    def __init__(self):
        super().__init__(
            name="Report Generator",
            role_description="Compiles all findings into a final JSON report",
            prompt_template=REPORT_GENERATOR_PROMPT
        )

    def generate_report(self, startup_idea, idea_analysis, market_research, 
                        business_strategy, financial_model, risk_assessment):
        """
        Generate a comprehensive report based on all analyses.
        
        Args:
            All ..._analysis args are now Python dictionaries (from loaded JSON)
            
        Returns:
            tuple: (final_report_dict, pdf_file_path)
        """
        
        # Combine all the structured data into one big dictionary
        full_analysis_dict = {
            "startup_idea": startup_idea,
            "idea_overview": idea_analysis,
            "market_landscape": market_research,
            "business_strategy": business_strategy,
            "financial_outlook": financial_model,
            "risk_assessment": risk_assessment
        }
        
        # Convert the dictionary to a JSON string to pass to the LLM
        combined_input_json = json.dumps(full_analysis_dict, indent=2)
        
        # Generate the final JSON (summary, verdict, rating, recommendations)
        final_report_json_string = self.run(combined_input_json)
        
        # Parse the final report
        final_report_dict = json.loads(final_report_json_string)
        
        # --- PDF Generation ---
        # Create a simple markdown string for the PDF
        pdf_markdown = f"# {final_report_dict.get('title', 'Startup Idea Validation Report')}\n\n"
        pdf_markdown += f"## Executive Summary\n{final_report_dict.get('executive_summary', '')}\n\n"
        pdf_markdown += f"## Final Verdict\n**Rating: {final_report_dict.get('overall_viability_rating', 'N/A')}/10**\n{final_report_dict.get('final_verdict', '')}\n\n"
        pdf_markdown += f"## Recommendations\n" + "\n".join(f"- {rec}" for rec in final_report_dict.get('recommendations', []))
        # You would add the other sections here if needed for the PDF
        
        report_file_path = create_pdf_report(startup_idea, pdf_markdown)
        
        # --- Return BOTH the full structured data and the final summary data ---
        
        master_report_dict = {
            "summary_data": final_report_dict,
            "detailed_data": full_analysis_dict
        }
        
        return master_report_dict, report_file_path