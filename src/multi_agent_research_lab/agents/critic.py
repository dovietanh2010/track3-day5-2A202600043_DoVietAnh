from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient


class CriticAgent(BaseAgent):
    """Optional fact-checking and safety-review agent."""

    name = "critic"

    def __init__(self, llm: LLMClient):
        self.llm = llm

    def run(self, state: ResearchState) -> ResearchState:
        """Validate final answer and append findings."""
        
        if not state.final_answer or not state.research_notes:
            state.errors.append("Critic ran with missing inputs.")
            return state
            
        system_prompt = (
            "You are a professional fact-checker. Your goal is to review a final report against research notes "
            "to ensure accuracy, identify hallucinations, and verify citation coverage."
        )
        user_prompt = (
            f"Research Notes:\n{state.research_notes}\n\n"
            f"Final Report:\n{state.final_answer}\n\n"
            "Please provide a critique of the final report. Are there any factual errors? Is anything missing? "
            "Is the citation coverage adequate?"
        )
        
        response = self.llm.complete(system_prompt, user_prompt)
        # Store critique in trace or a new state field if we had one
        state.add_trace_event(self.name, {"critique": response.content})
        
        return state
