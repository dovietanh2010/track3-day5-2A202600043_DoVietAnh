import logging
from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.config import get_settings
from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient

logger = logging.getLogger(__name__)


class SupervisorAgent(BaseAgent):
    """Decides which worker should run next and when to stop."""

    name = "supervisor"

    def __init__(self, llm: LLMClient):
        self.llm = llm
        self.max_iterations = get_settings().max_iterations

    def run(self, state: ResearchState) -> ResearchState:
        """Update `state.route_history` with the next route."""
        
        if state.iteration >= self.max_iterations:
            logger.warning(f"Reached max iterations ({self.max_iterations}). Ending workflow.")
            state.record_route("end")
            return state

        system_prompt = (
            "You are a workflow supervisor. Your task is to look at the current state of a research project "
            "and decide which expert to call next. Options are: 'researcher', 'analyst', 'writer', or 'end'.\n\n"
            "Guidelines:\n"
            "1. If research hasn't been done or more info is needed, call 'researcher'.\n"
            "2. If research is done but not analyzed, call 'analyst'.\n"
            "3. If analysis is done but final report is missing or needs work, call 'writer'.\n"
            "4. If the final report is complete and satisfactory, call 'end'.\n"
            "Output ONLY the name of the next agent (researcher, analyst, writer, end)."
        )
        
        user_prompt = (
            f"Query: {state.request.query}\n"
            f"Iteration: {state.iteration}\n"
            f"Has Research Notes: {bool(state.research_notes)}\n"
            f"Has Analysis Notes: {bool(state.analysis_notes)}\n"
            f"Has Final Answer: {bool(state.final_answer)}\n"
            f"Current Route History: {state.route_history}\n"
        )
        
        response = self.llm.complete(system_prompt, user_prompt)
        next_step = response.content.strip().lower()
        
        # Validation
        if next_step not in ["researcher", "analyst", "writer", "end"]:
            logger.error(f"Supervisor returned invalid route: {next_step}. Falling back to 'end'.")
            next_step = "end"
            
        state.record_route(next_step)
        state.add_trace_event(self.name, {"decision": next_step, "iteration": state.iteration})
        
        return state
