"""
PDF report generation utility for the Startup Idea Validator.
This version REMOVES all font downloading and sanitizes text
to be compatible with the built-in latin-1 font, preventing crashes.
"""

import os
import time
from fpdf import FPDF
import re
import json

from config import OUTPUT_DIR

def sanitize_text(text):
    """
    Removes all non-latin-1 characters to prevent PDF generation errors.
    This will strip emojis, special currency symbols (like ₹), etc.
    """
    return text.encode('latin-1', 'ignore').decode('latin-1')

def write_pretty_json(pdf, data):
    """
    Intelligently formats and writes a dictionary to the PDF,
    sanitizing all text for latin-1.
    """
    pdf.set_font('Arial', '', 10)
    
    if not isinstance(data, dict):
        pdf.write_body(str(data)) # write_body will sanitize
        return

    for key, value in data.items():
        pdf.set_font('Arial', 'B', 11)
        display_key = key.replace('_', ' ').title()
        pdf.cell(0, 7, sanitize_text(display_key), 0, 1)
        
        pdf.set_font('Arial', '', 10)
        
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    for sub_key, sub_val in item.items():
                         pdf.multi_cell(0, 5, sanitize_text(f"  - {sub_key.title()}: {sub_val}"))
                    pdf.ln(2)
                else:
                    pdf.multi_cell(0, 5, sanitize_text(f"- {item}"))
            pdf.ln(3)
        elif isinstance(value, dict):
            for sub_key, sub_val in value.items():
                pdf.multi_cell(0, 5, sanitize_text(f"  - {sub_key.title()}: {sub_val}"))
            pdf.ln(3)
        else:
            pdf.multi_cell(0, 5, sanitize_text(str(value)))
            pdf.ln(3)

class PDF(FPDF):
    """Custom PDF class, uses built-in Arial font ONLY."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.startup_name = "Startup Idea"
        self.set_font('Arial', '', 11) # Set default font

    def set_startup_name(self, name):
        self.startup_name = sanitize_text(name)

    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Startup Idea Validator Report', 0, 1, 'C')
        self.set_font('Arial', 'I', 8)
        self.cell(0, 5, f'Idea: {self.startup_name}', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 16)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 12, f' {sanitize_text(title)}', 0, 1, 'L', fill=True)
        self.ln(4)

    def sub_heading(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 8, sanitize_text(title), 0, 1, 'L')
        self.ln(2)

    def write_body(self, text):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 5, sanitize_text(text))
        self.ln()

    def add_swot(self, swot_data):
        if not isinstance(swot_data, dict):
            write_pretty_json(self, swot_data); return
        
        for section, items in swot_data.items():
            self.set_font('Arial', 'B', 11)
            self.cell(0, 7, sanitize_text(section.title()), 0, 1)
            self.set_font('Arial', '', 10)
            text = "\n".join(f"- {s}" for s in items)
            self.multi_cell(0, 5, sanitize_text(text))
            self.ln(2)

    def add_risks(self, risks_data):
        if not isinstance(risks_data, list):
            write_pretty_json(self, risks_data); return

        for risk in risks_data:
            rating = risk.get("rating", "N/A").lower()
            if rating == "high": self.set_text_color(220, 50, 50)
            elif rating == "medium": self.set_text_color(255, 165, 0)
            else: self.set_text_color(70, 130, 180)
            
            self.sub_heading(f"{sanitize_text(risk.get('category'))} ({sanitize_text(rating.title())} Risk)")
            self.set_text_color(0, 0, 0)
            self.write_body(f"**Risk:** {risk.get('risk', 'N/A')}\n**Mitigation:** {risk.get('mitigation', 'N/A')}")
            self.ln(2)

def sanitize_filename(text):
    """Convert text to a valid filename."""
    name = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '_', name)[:50]

def create_pdf_report(master_report_dict):
    """
    Create a comprehensive PDF report from the master report dictionary.
    """
    summary_data = master_report_dict.get("summary_data", {})
    details = master_report_dict.get("detailed_data", {})
    title = summary_data.get("title", "Startup Idea")
    
    pdf = PDF()
    pdf.set_startup_name(title)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    pdf.set_font('Arial', 'B', 24)
    pdf.cell(0, 15, sanitize_text(title), 0, 1, "C")
    pdf.ln(5)

    pdf.chapter_title("Executive Summary")
    pdf.write_body(summary_data.get("executive_summary", "No summary provided."))

    pdf.chapter_title("Final Verdict & Rating")
    rating = summary_data.get('overall_viability_rating', 0)
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, f"Overall Viability Rating: {rating} / 10", 0, 1, "L")
    pdf.write_body(summary_data.get("final_verdict", "No verdict provided."))

    pdf.chapter_title("Recommendations")
    recs = summary_data.get("recommendations", [])
    for i, rec in enumerate(recs, 1):
        pdf.write_body(f"{i}. {rec}")
    
    pdf.add_page()
    pdf.chapter_title("Detailed Analysis")
    pdf.sub_heading("Idea Overview")
    write_pretty_json(pdf, details.get("idea_overview", {}))
    pdf.sub_heading("Market Landscape")
    write_pretty_json(pdf, details.get("market_landscape", {}))

    pdf.add_page()
    pdf.chapter_title("Strategic & Financial Analysis")
    pdf.sub_heading("SWOT Analysis")
    pdf.add_swot(details.get("business_strategy", {}).get("swot", {}))
    pdf.sub_heading("Financial Outlook")
    write_pretty_json(pdf, details.get("financial_outlook", {}))

    pdf.add_page()
    pdf.chapter_title("Risk Assessment")
    pdf.add_risks(details.get("risk_assessment", []))

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"validation_report_{sanitize_filename(title)}_{timestamp}.pdf"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    try:
        # We sanitize *all text* before output, so this should not fail.
        pdf.output(filepath)
    except Exception as e:
        print(f"ERROR generating PDF: {e}")
        # Fallback to a simple text file if PDF generation fails
        filepath_txt = filepath.replace(".pdf", ".txt")
        with open(filepath_txt, "w", encoding='utf-8') as f:
            f.write(json.dumps(master_report_dict, indent=2))
        return filepath_txt
        
    return filepath