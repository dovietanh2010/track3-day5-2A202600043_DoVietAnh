from multi_agent_research_lab.agents import SupervisorAgent
from multi_agent_research_lab.core.schemas import ResearchQuery
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient

def test_supervisor_initialization() -> None:
    llm = LLMClient()
    supervisor = SupervisorAgent(llm=llm)
    assert supervisor.llm == llm

def test_supervisor_decision_schema() -> None:
    state = ResearchState(request=ResearchQuery(query="Testing query longer than 5 chars"))
    llm = LLMClient()
    supervisor = SupervisorAgent(llm=llm)
    # Just check it exists
    assert hasattr(supervisor, 'run')
