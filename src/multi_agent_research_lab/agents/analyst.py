from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient


class AnalystAgent(BaseAgent):
    """Turns research notes into structured insights."""

    name = "analyst"

    def __init__(self, llm: LLMClient):
        self.llm = llm

    def run(self, state: ResearchState) -> ResearchState:
        """Populate `state.analysis_notes`."""
        
        if not state.research_notes:
            state.errors.append("Analyst ran without research notes.")
            return state
            
        system_prompt = "You are a professional analyst. Your goal is to evaluate research notes, identify patterns, compare viewpoints, and extract key insights."
        user_prompt = f"Research Notes:\n{state.research_notes}\n\nPlease provide a structured analysis highlighting key insights, potential biases, and gaps in the research."
        
        response = self.llm.complete(system_prompt, user_prompt)
        state.analysis_notes = response.content
        
        state.add_trace_event(self.name, {"analysis_length": len(response.content)})
        
        return state
