from typing import Dict, Any
from langgraph.graph import StateGraph, END

from multi_agent_research_lab.agents.analyst import AnalystAgent
from multi_agent_research_lab.agents.critic import CriticAgent
from multi_agent_research_lab.agents.researcher import ResearcherAgent
from multi_agent_research_lab.agents.supervisor import SupervisorAgent
from multi_agent_research_lab.agents.writer import WriterAgent
from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient
from multi_agent_research_lab.services.search_client import SearchClient


class MultiAgentWorkflow:
    """Builds and runs the multi-agent graph."""

    def __init__(self) -> None:
        self.llm = LLMClient()
        self.search = SearchClient()
        
        self.supervisor = SupervisorAgent(self.llm)
        self.researcher = ResearcherAgent(self.llm, self.search)
        self.analyst = AnalystAgent(self.llm)
        self.writer = WriterAgent(self.llm)
        self.critic = CriticAgent(self.llm)

    def build(self) -> Any:
        """Create a LangGraph graph."""
        
        workflow = StateGraph(ResearchState)

        # Define nodes
        workflow.add_node("supervisor", self.supervisor.run)
        workflow.add_node("researcher", self.researcher.run)
        workflow.add_node("analyst", self.analyst.run)
        workflow.add_node("writer", self.writer.run)
        workflow.add_node("critic", self.critic.run)

        # Set entry point
        workflow.set_entry_point("supervisor")

        # Define conditional edges from supervisor
        workflow.add_conditional_edges(
            "supervisor",
            lambda x: x.route_history[-1],
            {
                "researcher": "researcher",
                "analyst": "analyst",
                "writer": "writer",
                "critic": "critic",
                "end": END
            }
        )

        # Worker nodes always go back to supervisor
        workflow.add_edge("researcher", "supervisor")
        workflow.add_edge("analyst", "supervisor")
        workflow.add_edge("writer", "supervisor")
        workflow.add_edge("critic", "supervisor")

        return workflow.compile()

    def run(self, state: ResearchState) -> ResearchState:
        """Execute the graph and return final state."""
        
        graph = self.build()
        result = graph.invoke(state)
        
        # In LangGraph, invoke returns the final state (usually a dict or the state object)
        if isinstance(result, dict):
            return ResearchState(**result)
        return result
