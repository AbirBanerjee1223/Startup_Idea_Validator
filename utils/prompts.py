"""
Updated prompts for structured JSON output.
"""
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# --- IDEA ANALYST (Returns JSON) ---
IDEA_ANALYST_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an Idea Analyst. Analyze the startup idea and return a JSON object.
Example:
{
  "problem": "What problem does it solve?",
  "target_audience": "Who are the users/customers?",
  "domain": "What industry is this in?",
  "solution": "How does it solve the problem?",
  "value_proposition": "What unique value does it offer?",
  "core_technologies": "What technologies does it use?"
}"""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "Startup Idea:\n{input}")
])

# --- MARKET RESEARCHER (Returns JSON) ---
MARKET_RESEARCHER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a Market Researcher. Based on the startup idea, return a JSON object.
Example:
{
  "market_size": "Estimate the Total Addressable Market.",
  "competitors": ["List 3-5 major competitors."],
  "market_trends": ["Key current and future trends."],
  "market_gaps": ["Unmet needs or opportunities."],
  "barriers_to_entry": ["Challenges for new entrants."],
  "target_market_profile": "Demographics and psychographics."
}"""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "Startup Idea:\n{input}")
])

# --- BUSINESS STRATEGIST (Returns JSON for SWOT) ---
BUSINESS_STRATEGIST_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a Business Strategist. Provide a SWOT analysis and other strategies as a JSON object.
Example:
{
  "swot": {
    "strengths": ["Internal advantage 1", "Internal advantage 2"],
    "weaknesses": ["Internal limitation 1"],
    "opportunities": ["External favorable factor 1"],
    "threats": ["External unfavorable factor 1"]
  },
  "product_market_fit": "Your assessment text here...",
  "go_to_market_strategy": "Your strategy text here...",
  "competitive_advantage": "Your assessment text here...",
  "growth_strategy": "Your strategy text here..."
}"""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "Information:\n{input}")
])

# --- FINANCIAL MODELER (Returns JSON) ---
FINANCIAL_MODELER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a Financial Modeling expert. Provide a financial outlook as a JSON object.
Example:
{
  "monetization_models": [
    {"model": "Model 1", "pros": "...", "cons": "..."},
    {"model": "Model 2", "pros": "...", "cons": "..."}
  ],
  "funding_requirements": "Estimate of initial funding needed (e.g., '$1.5M - $2M').",
  "revenue_projections": "High-level 3-year projection scenario.",
  "key_expenses": ["Major cost category 1", "Major cost category 2"],
  "funding_strategy": "Recommended funding sources (e.g., 'Seed round, Angel investors')."
}"""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "Analyses:\n{input}")
])

# --- RISK ASSESSOR (Returns JSON list) ---
RISK_ASSESSOR_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a Risk Assessment Specialist. Identify risks and return a JSON list.
Example:
[
  {"category": "Technical", "risk": "Dependency on AI accuracy.", "rating": "High", "mitigation": "Strategy to mitigate..."},
  {"category": "Market", "risk": "Competition from incumbents.", "rating": "High", "mitigation": "Strategy to mitigate..."},
  {"category": "Financial", "risk": "Cash flow issues.", "rating": "Medium", "mitigation": "Strategy to mitigate..."}
]"""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "Analyses:\n{input}")
])

# --- REPORT GENERATOR (Returns JSON) ---
REPORT_GENERATOR_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a Report Writer. You will receive structured JSON data from other agents.
Your job is to:
1.  Synthesize a 2-3 sentence 'executive_summary'.
2.  Synthesize a 'final_verdict' paragraph.
3.  Provide an 'overall_viability_rating' (a number from 1 to 10).
4.  Provide a list of 3-5 'recommendations' (actionable next steps).
5.  Extract the startup name for the 'title'.

Return ONLY a valid JSON object with these keys.
Example:
{
  "title": "ReWardrobe",
  "executive_summary": "...",
  "final_verdict": "...",
  "overall_viability_rating": 8,
  "recommendations": ["Develop an MVP...", "Secure seed funding...", "Build a community..."]
}"""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "All analyses as a JSON string:\n{input}")
])