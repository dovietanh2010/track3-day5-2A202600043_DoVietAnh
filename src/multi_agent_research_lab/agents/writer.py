from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient


class WriterAgent(BaseAgent):
    """Produces final answer from research and analysis notes."""

    name = "writer"

    def __init__(self, llm: LLMClient):
        self.llm = llm

    def run(self, state: ResearchState) -> ResearchState:
        """Populate `state.final_answer`."""
        
        if not state.research_notes or not state.analysis_notes:
            state.errors.append("Writer ran with missing inputs.")
            
        system_prompt = "You are a professional writer. Your goal is to synthesize research and analysis into a polished, final report that directly answers the user's query."
        user_prompt = (
            f"User Query: {state.request.query}\n\n"
            f"Research Notes:\n{state.research_notes}\n\n"
            f"Analysis Notes:\n{state.analysis_notes}\n\n"
            "Please write a comprehensive final report. Include citations to sources where appropriate."
        )
        
        response = self.llm.complete(system_prompt, user_prompt)
        state.final_answer = response.content
        
        state.add_trace_event(self.name, {"answer_length": len(response.content)})
        
        return state
