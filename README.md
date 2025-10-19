# Startup Idea Validator (SIV)

A LLM-powered multi-agent system that automatically evaluates and validates early-stage startup ideas, providing comprehensive analysis within minutes.

## 🧠 Overview

The Startup Idea Validator helps entrepreneurs, investors, and innovators quickly assess the viability of startup ideas by simulating expert analysis across multiple domains:

  * Problem and solution analysis
  * Market research and competitor analysis
  * Business strategy development and SWOT analysis
  * Financial modeling and monetization strategies
  * Risk assessment and mitigation planning

The system uses a team of specialized AI agents, powered by Google's Gemini model, to collaborate and build a comprehensive validation report from a single user prompt.

## 🛠️ Tech Stack

  * **Core Framework:** [LangChain](https://python.langchain.com/) 
  * **LLM:** [Google Gemini API](https://ai.google.dev/) (e.g., `gemini-pro-latest`)
  * **Core Development:** Python 3.9+
  * **Web Interface:** Streamlit
  * **Report Generation:** FPDF
  * **Web Search:** Tavily AI (for future integration)

## 🚀 Getting Started

### Prerequisites

  * Python 3.9+
  * A Google Gemini API key (get one from [Google AI Studio](https://ai.google.dev/))
  * A Tavily AI API key (for web search features)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/AbirBanerjee1223/Startup_Idea_Validator.git
    cd Startup_Idea_Validator
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv myenv
    source myenv/bin/activate  # On Windows: myenv\Scripts\activate
    ```

3.  **Install dependencies:**
    (Make sure your `requirements.txt` file is up-to-date with `langchain-google-genai`, `langchain-core`, etc.)

    ```bash
    pip install -r requirements.txt
    ```

4.  **Create a `.env` file:**
    Create a file named `.env` in the root directory and add your API keys:

    ```
    GEMINI_API_KEY="your_gemini_api_key_here"
    TAVILY_API_KEY="your_tavily_api_key_here"
    ```

### Running the Application

This project can be run as a command-line script (for testing) or as a Streamlit web app (for interaction).

1.  **Web Interface (Recommended):**
    Launch the Streamlit web app:

    ```bash
    streamlit run app.py
    ```

    Then open your browser to `http://localhost:8501`.

2.  **Command Line Interface:**
    Run a validation directly from the command line using the sample idea in `main.py`:

    ```bash
    python main.py
    ```

    This will run the test and save the output PDF to the `output_reports/` directory.

## 👨‍💻 System Architecture

### Core Agents

  * **Idea Analyst:** Breaks down the startup idea into its core components (problem, audience, solution).
  * **Market Researcher:** Analyzes the market, competitors, and trends based on the idea's components.
  * **Business Strategist:** Conducts a SWOT analysis and assesses product-market fit.
  * **Financial Modeler:** Suggests monetization models, funding requirements, and revenue projections.
  * **Risk Assessor:** Highlights potential technical, legal, and market risks.
  * **Report Generator:** Compiles all findings into a concise, professional evaluation report.

### Workflow Overview

1.  **User Input:** A user enters their startup idea via the Streamlit UI.
2.  **Multi-Agent Pipeline:** The `main.py` orchestrator feeds the idea to the first agent (`IdeaAnalyst`). The output from each agent is passed as input to the next in a sequential pipeline.
3.  **Agent Memory:** Each agent uses a modern LCEL chain with `RunnableWithMessageHistory` to maintain its own independent conversation history, allowing it to build upon its previous analysis.
4.  **Report Generation:** The final `ReportGenerator` agent receives the complete analysis from all other agents and compiles it into a single, comprehensive report.
5.  **Output:** The user receives the final validation report in both Markdown (on-screen) and as a downloadable PDF document.

## 📄 Example Output

The final report includes:

  * 🔍 **Executive Summary**
  * 💡 **Idea Overview**
  * 📊 **Market Landscape**
  * ⚖️ **SWOT Analysis**
  * 💰 **Financial Outlook**
  * 🚨 **Risk Assessment**
  * 📋 **Final Verdict & Recommendations**

## 🤝 Contributing

Contributions are welcome\! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the `LICENSE` file for details.
