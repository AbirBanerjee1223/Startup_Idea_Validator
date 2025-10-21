"""
Streamlit web interface for the Startup Idea Validator.
"""
import os
import streamlit as st
import time
import base64

from main import validate_startup_idea
from config import STREAMLIT_TITLE, STREAMLIT_DESCRIPTION


def display_pdf(file_path):
    """
    Display a PDF file in Streamlit.
    
    Args:
        file_path (str): Path to the PDF file
    """
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    
    # Embed PDF viewer
    pdf_display = f"""
        <iframe 
            src="data:application/pdf;base64,{base64_pdf}" 
            width="100%" 
            height="600" 
            type="application/pdf">
        </iframe>
    """
    st.markdown(pdf_display, unsafe_allow_html=True)


def display_risks(risks_list):
    """Displays a list of risks with color-coded ratings."""
    if not isinstance(risks_list, list):
        st.error("Risk assessment data is not formatted correctly.")
        st.json(risks_list) # Show what was received
        return

    for risk in risks_list:
        if not isinstance(risk, dict): continue
        
        rating = risk.get("rating", "N/A").lower()
        if rating == "high":
            st.error(f"**{risk.get('category', 'Risk')} (Rating: High):** {risk.get('risk', 'N/A')}")
        elif rating == "medium":
            st.warning(f"**{risk.get('category', 'Risk')} (Rating: Medium):** {risk.get('risk', 'N/A')}")
        else:
            st.info(f"**{risk.get('category', 'Risk')} (Rating: {rating.title()}):** {risk.get('risk', 'N/A')}")
        
        if risk.get("mitigation"):
            with st.expander("Suggested Mitigation"):
                st.write(risk.get("mitigation"))


def display_swot(swot_dict):
    """Displays SWOT analysis in two columns."""
    if not isinstance(swot_dict, dict):
        st.error("SWOT data is not formatted correctly.")
        st.json(swot_dict) # Show what was received
        return

    col1, col2 = st.columns(2)
    with col1:
        st.success("**Strengths**")
        st.markdown("\n".join(f"- {s}" for s in swot_dict.get("strengths", [])))
        
        st.info("**Opportunities**")
        st.markdown("\n".join(f"- {o}" for o in swot_dict.get("opportunities", [])))
    
    with col2:
        st.error("**Weaknesses**")
        st.markdown("\n".join(f"- {w}" for w in swot_dict.get("weaknesses", [])))
        
        st.warning("**Threats**")
        st.markdown("\n".join(f"- {t}" for t in swot_dict.get("threats", [])))


def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title=STREAMLIT_TITLE,
        page_icon="🚀",
        layout="wide"
    )
    
    st.title(f"🚀 {STREAMLIT_TITLE}")
    st.markdown(STREAMLIT_DESCRIPTION)
    
    st.warning("⚠️ This application uses the Gemini API, which may take a moment to generate a complete report. Please be patient during processing.")
    
    # Input form
    with st.form("startup_idea_form"):
        startup_idea = st.text_area(
            "Describe your startup idea in detail",
            height=150,
            placeholder="Example: An AI-powered mobile app that helps users resell their used clothing by auto-generating listings..."
        )
        
        submit_button = st.form_submit_button("Validate My Startup Idea")
    
    # Process on submit
    if submit_button and startup_idea:
        with st.spinner("Our AI agents are analyzing your startup idea... This may take a moment with the Gemini model."):
            try:
                # Simulate agent progress for UI feedback
                progress_bar = st.progress(0)
                status_text = st.empty()
                steps = ["Analyzing idea...", "Researching market...", "Developing strategy...", "Modeling financials...", "Assessing risks...", "Generating final report..."]
                
                report_dict, report_path = None, None
                for i, step in enumerate(steps):
                    status_text.text(f"Step {i+1}/{len(steps)}: {step}")
                    progress_bar.progress((i + 1) / len(steps))
                    if i == 0: # Run the actual validation on the first step
                        report_dict, report_path = validate_startup_idea(startup_idea)
                    else: # Simulate time for other steps
                        time.sleep(1)
                
                status_text.text("Analysis complete!")
                st.success("Startup idea validation complete!")
                
                # --- NEW DISPLAY LOGIC ---
                
                summary_data = report_dict.get("summary_data", {})
                details = report_dict.get("detailed_data", {})

                report_tab, pdf_tab = st.tabs(["📊 Validation Report", "📄 PDF Document"])
                
                with report_tab:
                    st.header(summary_data.get("title", "Validation Report"))
                    
                    rating = summary_data.get('overall_viability_rating', 0)
                    st.metric(label="Overall Viability Rating", value=f"{rating} / 10")
                    st.progress(rating / 10)

                    st.subheader("Executive Summary")
                    st.write(summary_data.get("executive_summary", "No summary provided."))
                    
                    st.subheader("Final Verdict")
                    st.write(summary_data.get("final_verdict", "No verdict provided."))
                    
                    st.divider()
                    
                    st.header("Recommendations")
                    recs = summary_data.get("recommendations", [])
                    for i, rec in enumerate(recs, 1):
                        st.info(f"**Step {i}:** {rec}")
                    
                    st.divider()

                    st.header("Detailed Analysis")

                    with st.expander("💡 Idea Overview", expanded=True):
                        st.json(details.get("idea_overview", {}))

                    with st.expander("📈 Market Landscape"):
                        st.json(details.get("market_landscape", {}))
                    
                    with st.expander("⚖️ SWOT Analysis"):
                        swot_data = details.get("business_strategy", {}).get("swot", {})
                        display_swot(swot_data)
                        # Optionally display the rest of the strategy info
                        # st.write("**Other Strategic Analysis:**")
                        # st.json(details.get("business_strategy", {}))

                    with st.expander("💰 Financial Outlook"):
                        fin_data = details.get("financial_outlook", {})
                        st.metric("Funding Requirements", fin_data.get("funding_requirements", "N/A"))
                        st.subheader("Monetization Models")
                        st.json(fin_data.get("monetization_models", []))
                        st.subheader("Key Expenses")
                        st.json(fin_data.get("key_expenses", []))

                    with st.expander("🚨 Risk Assessment"):
                        risk_data = details.get("risk_assessment", [])
                        display_risks(risk_data)

                with pdf_tab:
                    st.markdown("### PDF Report")
                    display_pdf(report_path)
                
            except Exception as e:
                st.error(f"An error occurred during validation: {str(e)}")
    
    st.markdown("---")
    st.markdown("### Tips for better results:\n- Be as specific as possible.\n- Include your target audience and the problem you're solving.\n- Describe your planned business model.")

if __name__ == "__main__":
    main()
