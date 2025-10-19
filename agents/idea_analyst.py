"""
Idea Analyst Agent for the Startup Idea Validator.
"""
from . import BaseAgent
from utils.prompts import IDEA_ANALYST_PROMPT


class IdeaAnalyst(BaseAgent):
    """
    Agent responsible for breaking down the startup idea into its core components:
    problem statement, target audience, domain, and proposed solution.
    """
    
    def __init__(self):
        super().__init__(
            name="Idea Analyst",
            role_description="Breaks down startup ideas into problem, audience, domain, and solution",
            prompt_template=IDEA_ANALYST_PROMPT
        )

    def analyze_idea(self, startup_idea):
        """
        Analyze the startup idea and break it down into components.
        
        Args:
            startup_idea (str): The raw startup idea description
            
        Returns:
            str: Structured analysis of the idea
        """
        return self.run(startup_idea)