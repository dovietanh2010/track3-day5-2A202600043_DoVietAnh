from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient
from multi_agent_research_lab.services.search_client import SearchClient


class ResearcherAgent(BaseAgent):
    """Collects sources and creates concise research notes."""

    name = "researcher"

    def __init__(self, llm: LLMClient, search: SearchClient):
        self.llm = llm
        self.search = search

    def run(self, state: ResearchState) -> ResearchState:
        """Populate `state.sources` and `state.research_notes`."""
        
        query = state.request.query
        
        # 1. Search for sources
        sources = self.search.search(query)
        state.sources.extend(sources)
        
        # 2. Synthesize research notes
        source_text = "\n\n".join([f"Source: {s.title}\nURL: {s.url}\nContent: {s.content}" for s in sources])
        
        system_prompt = "You are a professional researcher. Your goal is to synthesize findings from search results into concise, factual research notes."
        user_prompt = f"Query: {query}\n\nSearch Results:\n{source_text}\n\nPlease provide detailed research notes highlighting key findings and facts."
        
        response = self.llm.complete(system_prompt, user_prompt)
        state.research_notes = response.content
        
        state.add_trace_event(self.name, {"sources_found": len(sources), "notes_length": len(response.content)})
        
        return state
