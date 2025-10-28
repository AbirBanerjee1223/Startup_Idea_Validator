"""
Streamlit web interface for the Startup Idea Validator.
"""
import os
import streamlit as st
import time
import base64
import json
from main import validate_startup_idea
from config import STREAMLIT_TITLE, STREAMLIT_DESCRIPTION

# --- Page Configuration ---
st.set_page_config(
    page_title=STREAMLIT_TITLE,
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Agent Icons ---
AGENT_ICONS = {
    "Analyzing idea...": "🔬",
    "Researching market...": "📈",
    "Developing strategy...": "♟️",
    "Modeling financials...": "💰",
    "Assessing risks...": "🛡️",
    "Generating final report...": "✍️"
}

# --- Custom CSS (from previous step, unchanged) ---
def load_css():
    st.markdown("""
        <style>
            /* (Your existing CSS from the previous step goes here) */
            /* ... */
            :root {
                --background-color: #f0f2f6;
                /* ... etc ... */
            }
            [data-theme="dark"] {
                --background-color: #0E1117;
                /* ... etc ... */
            }
            .stExpander, .stForm, [data-testid="stMetric"], .stTabs, [data-testid="stSidebar"] {
                background-color: var(--card-background-color);
                border: 1px solid var(--card-border-color);
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                transition: box-shadow 0.3s ease-in-out;
            }
        </style>
    """, unsafe_allow_html=True)

# --- UI Helper Functions ---

# REMOVED the broken `display_pdf` function

def display_risks(risks_list):
    """Displays a list of risks with color-coded ratings."""
    if not isinstance(risks_list, list):
        st.error("Risk assessment data is not formatted correctly."); st.json(risks_list)
        return
    for risk in risks_list:
        if isinstance(risk, dict):
            rating = risk.get("rating", "N/A").lower()
            icon = "🛡️"
            if rating == "high": icon = "🚨"
            elif rating == "medium": icon = "⚠️"
            st.info(f"**{risk.get('category', 'Risk')} (Rating: {rating.title()}):** {risk.get('risk', 'N/A')}", icon=icon)

def display_swot(swot_dict):
    """Displays SWOT analysis in two columns."""
    if not isinstance(swot_dict, dict):
        st.error("SWOT data is not formatted correctly."); st.json(swot_dict)
        return
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("👍 Strengths")
        st.markdown("\n".join(f"- {s}" for s in swot_dict.get("strengths", [])))
        st.subheader("📈 Opportunities")
        st.markdown("\n".join(f"- {o}" for o in swot_dict.get("opportunities", [])))
    with col2:
        st.subheader("👎 Weaknesses")
        st.markdown("\n".join(f"- {w}" for w in swot_dict.get("weaknesses", [])))
        st.subheader("📉 Threats")
        st.markdown("\n".join(f"- {t}" for t in swot_dict.get("threats", [])))

# --- NEW HELPER FUNCTIONS to replace st.json ---

def display_overview(overview_data):
    """Displays the Idea Overview in a clean format."""
    if not isinstance(overview_data, dict):
        st.error("Overview data is not formatted correctly."); st.json(overview_data)
        return
    
    st.info(f"**Problem:** {overview_data.get('problem', 'N/A')}")
    st.info(f"**Solution:** {overview_data.get('solution', 'N/A')}")
    
    col1, col2 = st.columns(2)
    col1.metric("Target Audience", overview_data.get('target_audience', 'N/A'))
    col2.metric("Domain", overview_data.get('domain', 'N/A'))
    
    st.subheader("Value Proposition")
    st.write(overview_data.get('value_proposition', 'N/A'))
    st.subheader("Core Technologies")
    st.write(overview_data.get('core_technologies', 'N/A'))

def display_market(market_data):
    """Displays the Market Landscape in a clean format."""
    if not isinstance(market_data, dict):
        st.error("Market data is not formatted correctly."); st.json(market_data)
        return

    st.metric("Estimated Market Size (TAM)", market_data.get('market_size', 'N/A'))
    
    st.subheader("Competitors")
    st.markdown("\n".join(f"- {c}" for c in market_data.get('competitors', [])))
    
    st.subheader("Market Trends")
    st.markdown("\n".join(f"- {t}" for t in market_data.get('market_trends', [])))

    st.subheader("Market Gaps")
    st.markdown("\n".join(f"- {g}" for g in market_data.get('market_gaps', [])))
    
    st.subheader("Barriers to Entry")
    st.markdown("\n".join(f"- {b}" for b in market_data.get('barriers_to_entry', [])))

def display_financials(fin_data):
    """Displays the Financial Outlook in a clean format."""
    if not isinstance(fin_data, dict):
        st.error("Financial data is not formatted correctly."); st.json(fin_data)
        return

    st.metric("Funding Requirements", fin_data.get("funding_requirements", "N/A"))
    
    st.subheader("Monetization Models")
    models = fin_data.get('monetization_models', [])
    for model in models:
        if isinstance(model, dict):
            st.markdown(f"**Model:** {model.get('model', 'N/A')}")
            with st.expander("Pros & Cons"):
                st.success(f"**Pros:** {model.get('pros', 'N/A')}")
                st.error(f"**Cons:** {model.get('cons', 'N/A')}")
        else:
            st.write(model)

    st.subheader("Key Expenses")
    st.markdown("\n".join(f"- {e}" for e in fin_data.get('key_expenses', [])))
    
    st.subheader("Funding Strategy")
    st.write(fin_data.get('funding_strategy', 'N/A'))

# --- Main Application ---
def main():
    load_css()

    with st.sidebar:
        st.image("https://i.imgur.com/M73fKkF.png", width=70)
        st.header("About SIV")
        st.info("This AI-powered multi-agent system validates startup ideas by simulating a team of experts.")
        st.markdown("---")
        st.subheader("Built By")
        st.write("Abir Banerjee")
        st.write("[GitHub](https://github.com/AbirBanerjee1223) | [LinkedIn](https://www.linkedin.com/in/abir-banerjee-a13a58231/)")

    st.title(f"🚀 {STREAMLIT_TITLE}")
    st.markdown(f"##### {STREAMLIT_DESCRIPTION}")
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.form("startup_idea_form"):
        st.subheader("Enter Your Startup Idea")
        startup_idea = st.text_area("Description", height=150, placeholder="e.g., An AI-powered app that resells used clothing...", label_visibility="collapsed")
        submit_button = st.form_submit_button("✨ Validate My Startup Idea!")

    if submit_button and startup_idea:
        report_dict, report_path = None, None
        status_container = st.empty()
        
        try:
            validation_generator = validate_startup_idea(startup_idea)
            
            for step_message in validation_generator:
                if isinstance(step_message, tuple):
                    report_dict, report_path = step_message
                    break
                
                with status_container:
                    with st.status(f"**Agent at work:** {step_message}", expanded=True) as status:
                        status.update(label=f"**{AGENT_ICONS.get(step_message, '⚙️')} {step_message.split('...')[0]} Complete!**", state="complete", expanded=False)
            
            status_container.success("✅ All agents have completed their analysis!")
            time.sleep(1)
            status_container.empty()

            summary_data = report_dict.get("summary_data", {})
            details = report_dict.get("detailed_data", {})

            st.header(f"💡 Validation Report for: **{summary_data.get('title', 'Your Idea')}**")
            
            report_tab, pdf_tab = st.tabs(["📊 Key Insights", "📄 Full Report PDF"])
            
            with report_tab:
                st.subheader("🎯 Executive Summary")
                st.write(summary_data.get("executive_summary", "No summary provided."))
                st.markdown("<br>", unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    rating = summary_data.get('overall_viability_rating', 0)
                    st.metric(label="Overall Viability Rating", value=f"{rating} / 10")
                    st.progress(rating / 10)
                with col2:
                    funding = details.get("financial_outlook", {}).get("funding_requirements", "N/A")
                    st.metric("Estimated Funding Required", funding)
                st.markdown("<br>", unsafe_allow_html=True)
                with st.container(border=True):
                    st.subheader("⭐ Final Verdict & Recommendations")
                    st.write(summary_data.get("final_verdict", "No verdict provided."))
                    st.divider()
                    recs = summary_data.get("recommendations", [])
                    for i, rec in enumerate(recs, 1):
                        st.success(f"**Step {i}:** {rec}", icon="➡️")
                st.markdown("<br>", unsafe_allow_html=True)
                
                # --- THIS IS THE FIX ---
                # Replaced all st.json calls with the new display functions
                st.header("🔬 Detailed Analysis")
                with st.expander("💡 Idea Overview", expanded=True):
                    display_overview(details.get("idea_overview", {}))
                with st.expander("📈 Market Landscape"):
                    display_market(details.get("market_landscape", {}))
                with st.expander("⚖️ SWOT Analysis"):
                    display_swot(details.get("business_strategy", {}).get("swot", {}))
                with st.expander("💰 Financial Outlook"):
                    display_financials(details.get("financial_outlook", {}))
                with st.expander("🚨 Risk Assessment"):
                    display_risks(details.get("risk_assessment", []))
            
            with pdf_tab:
                # --- THIS IS THE FIX ---
                # Replaced the broken iframe with a reliable download button
                st.subheader("Download Your Full Report")
                st.write("Click the button below to download the complete, multi-page PDF analysis.")
                
                try:
                    with open(report_path, "rb") as f:
                        pdf_data = f.read()
                    
                    st.download_button(
                        label="⬇️ Download PDF Report",
                        data=pdf_data,
                        file_name=os.path.basename(report_path),
                        mime="application/pdf"
                    )
                except FileNotFoundError:
                    st.error("Could not find the generated PDF file to create a download link.")
                except Exception as e:
                    st.error(f"An error occurred while preparing the PDF for download: {e}")
                
        except Exception as e:
            st.error(f"An error occurred during validation: {str(e)}")
            if report_dict: st.json(report_dict)

if __name__ == "__main__":
    main()