"""
Base agent implementation for the Startup Idea Validator.
"""
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from config import GROQ_API_KEY, MODEL_NAME, TEMPERATURE, MAX_TOKENS


class BaseAgent:
    """Base class for all agents in the Startup Idea Validator."""

    def __init__(self, name, role_description, prompt_template):
        """Initialize the agent with name, role and prompt template.
        
        Args:
            name (str): The name of the agent
            role_description (str): Description of the agent's role
            prompt_template (str): The prompt template for the agent
        """
        self.name = name
        self.role_description = role_description
        self.prompt_template = prompt_template
        self.llm = self._setup_llm()
        self.memory = ConversationBufferMemory(memory_key="chat_history")
        self.chain = self._setup_chain()
    
    def _setup_llm(self):
        """Set up the LLM for the agent."""
        return ChatGroq(
            model_name=MODEL_NAME,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            groq_api_key=GROQ_API_KEY,
        )
    
    def _setup_chain(self):
        """Set up the chain for the agent."""
        prompt = PromptTemplate(
            template=self.prompt_template,
            input_variables=["input", "chat_history"]
        )
        return LLMChain(
            llm=self.llm,
            prompt=prompt,
            memory=self.memory,
            verbose=True
        )
    
    def run(self, input_text):
        """Run the agent on the input text."""
        return self.chain.run(input=input_text)