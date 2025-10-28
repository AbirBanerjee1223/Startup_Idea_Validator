"""
Base agent implementation for the Startup Idea Validator.
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.messages import HumanMessage, AIMessage

from config import GEMINI_API_KEY, MODEL_NAME, TEMPERATURE

class BaseAgent:
    """Base class for all agents in the Startup Idea Validator."""
    
    # Class-level dictionary to store chat histories for each agent instance
    agent_histories = {}

    def __init__(self, name, role_description, prompt_template):
        """Initialize the agent."""
        self.name = name
        self.role_description = role_description
        self.prompt = prompt_template
        self.llm = self._setup_llm()
        self.chain = self.prompt | self.llm | JsonOutputParser()
        
        # Each agent gets its own history list in the shared dictionary
        if self.name not in self.agent_histories:
            self.agent_histories[self.name] = []

    def _setup_llm(self):
        """Set up the LLM for the agent."""
        return ChatGoogleGenerativeAI(
            model=MODEL_NAME,
            temperature=TEMPERATURE,
            google_api_key=GEMINI_API_KEY,
            convert_system_message_to_human=True
        )

    def run(self, input_text):
        """Run the agent, manually managing the history."""
        
        # Get the specific history for this agent instance
        current_history = self.agent_histories[self.name]
        
        # Invoke the chain with the input and the current history
        output_dict = self.chain.invoke({
            "input": input_text,
            "chat_history": current_history
        })
        
        # Manually update the history
        current_history.append(HumanMessage(content=input_text))
        current_history.append(AIMessage(content=str(output_dict)))
        
        return output_dict