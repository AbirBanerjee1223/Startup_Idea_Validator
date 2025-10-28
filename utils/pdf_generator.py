"""
PDF report generation utility for the Startup Idea Validator.
This version includes Unicode font support with stable CDN links to handle emojis and special characters.
"""

import os
import time
from fpdf import FPDF
import re
import json
import requests

from config import OUTPUT_DIR

def setup_fonts(pdf):
    """Downloads and adds Unicode-compatible fonts from a stable CDN to the FPDF instance."""
    font_dir = os.path.join(os.path.dirname(__file__), "fonts")
    os.makedirs(font_dir, exist_ok=True)
    
    # --- THIS IS THE FIX ---
    # These URLs point to a reliable CDN (jsDelivr) instead of raw GitHub, which is more stable.
    font_files = {
        "NotoSans-Regular.ttf": "https://cdn.jsdelivr.net/gh/google/fonts@main/ofl/notosans/NotoSans-Regular.ttf",
        "NotoSans-Bold.ttf": "https://cdn.jsdelivr.net/gh/google/fonts@main/ofl/notosans/NotoSans-Bold.ttf",
        "NotoSans-Italic.ttf": "https://cdn.jsdelivr.net/gh/google/fonts@main/ofl/notosans/NotoSans-Italic.ttf"
    }

    for font_file, url in font_files.items():
        path = os.path.join(font_dir, font_file)
        if not os.path.exists(path):
            print(f"Downloading font: {font_file}...")
            try:
                response = requests.get(url, allow_redirects=True, timeout=10)
                response.raise_for_status()
                with open(path, 'wb') as f:
                    f.write(response.content)
            except requests.RequestException as e:
                print(f"Warning: Could not download font {font_file}. PDF may have rendering issues. Error: {e}")
                return False

    try:
        pdf.add_font('NotoSans', '', os.path.join(font_dir, "NotoSans-Regular.ttf"), uni=True)
        pdf.add_font('NotoSans', 'B', os.path.join(font_dir, "NotoSans-Bold.ttf"), uni=True)
        pdf.add_font('NotoSans', 'I', os.path.join(font_dir, "NotoSans-Italic.ttf"), uni=True)
        pdf.set_font('NotoSans', '', 11)
        return True
    except Exception as e:
        print(f"Warning: Could not load fonts. PDF may have rendering issues. Error: {e}")
        pdf.set_font('Arial', '', 11) # Fallback to Arial if loading fails
        return False


def write_pretty_json(pdf, data):
    """
    Intelligently formats and writes a dictionary to the PDF.
    Handles nested dictionaries, lists, and simple key-value pairs.
    """
    pdf.set_font('NotoSans' if pdf.has_unicode_support else 'Arial', '', 10)
    
    if not isinstance(data, dict):
        pdf.write_body(str(data))
        return

    for key, value in data.items():
        # --- Heading for the key ---
        pdf.set_font('NotoSans' if pdf.has_unicode_support else 'Arial', 'B', 11)
        # Clean up the key for display (e.g., "market_size" -> "Market Size")
        display_key = key.replace('_', ' ').title()
        pdf.cell(0, 7, display_key, 0, 1)
        
        # --- Value formatting ---
        pdf.set_font('NotoSans' if pdf.has_unicode_support else 'Arial', '', 10)
        
        if isinstance(value, list):
            # Handle lists (like competitors, market trends)
            for item in value:
                if isinstance(item, dict): # Handle list of objects (like monetization models)
                    for sub_key, sub_val in item.items():
                         pdf.multi_cell(0, 5, f"  - {sub_key.title()}: {sub_val}")
                    pdf.ln(2)
                else: # Handle list of strings
                    pdf.multi_cell(0, 5, f"- {item}")
            pdf.ln(3)

        elif isinstance(value, dict):
            # Handle nested dictionaries (like target_market_profile)
            for sub_key, sub_val in value.items():
                pdf.multi_cell(0, 5, f"  - {sub_key.title()}: {sub_val}")
            pdf.ln(3)
        
        else:
            # Handle simple string/number values
            pdf.multi_cell(0, 5, str(value))
            pdf.ln(3)

class PDF(FPDF):
    """Custom PDF class to handle headers, footers, and chapter titles."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.startup_name = "Startup Idea"
        self.has_unicode_support = setup_fonts(self)

    # --- (header, footer, chapter_title, etc. are unchanged) ---
    def set_startup_name(self, name):
        self.startup_name = name

    def header(self):
        self.set_font('NotoSans' if self.has_unicode_support else 'Arial', 'B', 12)
        self.cell(0, 10, 'Startup Idea Validator Report', 0, 1, 'C')
        self.set_font('NotoSans' if self.has_unicode_support else 'Arial', 'I', 8)
        self.cell(0, 5, f'Idea: {self.startup_name}', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('NotoSans' if self.has_unicode_support else 'Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('NotoSans' if self.has_unicode_support else 'Arial', 'B', 16)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 12, f' {title}', 0, 1, 'L', fill=True)
        self.ln(4)
        
    def _write_unicode(self, method, text):
        """Helper to write text, falling back if unicode fails."""
        if self.has_unicode_support:
            method(text)
        else:
            fallback_text = text.encode('latin-1', 'replace').decode('latin-1')
            method(fallback_text)

    def sub_heading(self, title):
        self.set_font('NotoSans' if self.has_unicode_support else 'Arial', 'B', 12)
        self._write_unicode(lambda t: self.cell(0, 8, t, 0, 1, 'L'), title)
        self.ln(2)

    def write_body(self, text):
        self.set_font('NotoSans' if self.has_unicode_support else 'Arial', '', 11)
        self._write_unicode(lambda t: self.multi_cell(0, 5, t), text)
        self.ln()

    def add_swot(self, swot_data):
        if not isinstance(swot_data, dict):
            write_pretty_json(self, swot_data); return
        
        for section, items in swot_data.items():
            self.set_font('NotoSans' if self.has_unicode_support else 'Arial', 'B', 11)
            self.cell(0, 7, section.title(), 0, 1)
            self.set_font('NotoSans' if self.has_unicode_support else 'Arial', '', 10)
            text = "\n".join(f"- {s}" for s in items)
            self._write_unicode(lambda t: self.multi_cell(0, 5, t), text)
            self.ln(2)

    def add_risks(self, risks_data):
        if not isinstance(risks_data, list):
            write_pretty_json(self, risks_data); return

        for risk in risks_data:
            rating = risk.get("rating", "N/A").lower()
            if rating == "high": self.set_text_color(220, 50, 50)
            elif rating == "medium": self.set_text_color(255, 165, 0)
            else: self.set_text_color(70, 130, 180)
            
            self.sub_heading(f"{risk.get('category')} ({rating.title()} Risk)")
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
    
    pdf.set_font('NotoSans' if pdf.has_unicode_support else 'Arial', 'B', 24)
    pdf.cell(0, 15, title, 0, 1, "C")
    pdf.ln(5)

    pdf.chapter_title("Executive Summary")
    pdf.write_body(summary_data.get("executive_summary", "No summary provided."))

    pdf.chapter_title("Final Verdict & Rating")
    rating = summary_data.get('overall_viability_rating', 0)
    pdf.set_font('NotoSans' if pdf.has_unicode_support else 'Arial', 'B', 14)
    pdf.cell(0, 10, f"Overall Viability Rating: {rating} / 10", 0, 1, "L")
    pdf.write_body(summary_data.get("final_verdict", "No verdict provided."))

    pdf.chapter_title("Recommendations")
    recs = summary_data.get("recommendations", [])
    for i, rec in enumerate(recs, 1):
        pdf.write_body(f"{i}. {rec}")
    
    # --- THIS IS THE FIX ---
    # Replace all `pdf.write_json_data` with `write_pretty_json`
    
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
        pdf.output(filepath)
    except Exception as e:
        print(f"ERROR generating PDF: {e}")
        filepath_txt = filepath.replace(".pdf", ".txt")
        with open(filepath_txt, "w", encoding='utf-8') as f: # Added encoding
            f.write(json.dumps(master_report_dict, indent=2))
        return filepath_txt
        
    return filepath
