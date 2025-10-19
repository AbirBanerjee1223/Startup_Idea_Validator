"""
Base agent implementation for the Startup Idea Validator.
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser

from config import GEMINI_API_KEY, MODEL_NAME, TEMPERATURE

class BaseAgent:
    """Base class for all agents in the Startup Idea Validator."""
    
    # Use a class-level dictionary to store chat histories for each agent
    session_store = {}

    def __init__(self, name, role_description, prompt_template):
        """Initialize the agent with name, role and prompt template.
        
        Args:
            name (str): The name of the agent
            role_description (str): Description of the agent's role
            prompt_template (ChatPromptTemplate): The prompt template object from utils.prompts
        """
        self.name = name
        self.role_description = role_description
        
        # The prompt_template is now a ChatPromptTemplate object
        self.prompt = prompt_template 
        self.llm = self._setup_llm()
        self.chain = self._setup_chain()
    
    def _setup_llm(self):
        """Set up the LLM for the agent."""
        return ChatGoogleGenerativeAI(
            model=MODEL_NAME,
            temperature=TEMPERATURE,
            google_api_key=GEMINI_API_KEY,
            convert_system_message_to_human=True
        )
    
    def get_session_history(self, session_id: str):
        """
        Factory function to get or create chat history for a session.
        This is required by RunnableWithMessageHistory.
        """
        if session_id not in self.session_store:
            self.session_store[session_id] = InMemoryChatMessageHistory()
        return self.session_store[session_id]

    def _setup_chain(self):
        """Set up the chain for the agent using LCEL and RunnableWithMessageHistory."""
        
        # Create the runnable chain
        runnable = self.prompt | self.llm | StrOutputParser()
        
        # Wrap the runnable with message history capabilities
        chain_with_history = RunnableWithMessageHistory(
            runnable,
            self.get_session_history,
            input_messages_key="input",          # The key for the user's new message
            history_messages_key="chat_history", # The key for the list of old messages
        )
        return chain_with_history
    
    def run(self, input_text):
        """Run the agent on the input text."""
        
        # The "session_id" is the agent's name.
        # This ensures each agent (Idea Analyst, Market Researcher, etc.)
        # has its own separate memory.
        config = {"configurable": {"session_id": self.name}}
        
        # Invoke the chain with the input and the session config
        # The runnable handles loading and saving the history automatically.
        return self.chain.invoke({"input": input_text}, config=config)