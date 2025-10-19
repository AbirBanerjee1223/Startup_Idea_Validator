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


def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title=STREAMLIT_TITLE,
        page_icon="🚀",
        layout="wide"
    )
    
    st.title(f"🚀 {STREAMLIT_TITLE}")
    st.markdown(STREAMLIT_DESCRIPTION)
    
    # Warning about processing time
    st.warning("⚠️ This application uses the Gemini API, which may take a moment to generate a complete report. Please be patient during processing.")
    
    # Input form
    with st.form("startup_idea_form"):
        startup_idea = st.text_area(
            "Describe your startup idea in detail",
            height=150,
            placeholder="Example: A mobile app that connects local farmers directly with consumers..."
        )
        
        # Form submission button
        submit_button = st.form_submit_button("Validate My Startup Idea")
    
    # Process on submit
    if submit_button and startup_idea:
        with st.spinner("Our AI agents are analyzing your startup idea... This may take a moment with the Gemini model."):
            try:
                # Create progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Simulate agent progress
                steps = [
                    "Analyzing idea components...",
                    "Researching market landscape...",
                    "Developing business strategy...",
                    "Creating financial models...",
                    "Assessing potential risks...",
                    "Generating final report..."
                ]
                
                # For each step, update progress bar
                for i, step in enumerate(steps):
                    status_text.text(step)
                    progress_bar.progress((i + 1) / len(steps))
                    
                    # Actually run the validation if this is the first step
                    if i == 0:
                        report_content, report_path = validate_startup_idea(startup_idea)
                    else:
                        # Just simulate time for UI feedback
                        time.sleep(1)
                
                # Show completion
                status_text.text("Analysis complete!")
                progress_bar.progress(100)
                
                # Display results
                st.success("Startup idea validation complete!")
                
                # Create tabs for different views
                report_tab, pdf_tab = st.tabs(["Report", "PDF Document"])
                
                with report_tab:
                    st.markdown(report_content)
                
                with pdf_tab:
                    st.markdown("### PDF Report")
                    st.markdown(f"Download link: [Validation Report]({report_path})")
                    display_pdf(report_path)
                
            except Exception as e:
                st.error(f"An error occurred during validation: {str(e)}")
    
    # Add some helpful information at the bottom
    st.markdown("---")
    st.markdown("""
    ### Tips for better results:
    
    - Be as specific as possible about your startup idea
    - Include your target audience and the problem you're solving
    - Mention any unique technology or approach you're using
    - Describe your planned business model or monetization strategy
    """)


if __name__ == "__main__":
    main()