import logging
from tavily import TavilyClient

from multi_agent_research_lab.core.config import get_settings
from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.schemas import SourceDocument

logger = logging.getLogger(__name__)


class SearchClient:
    """Provider-agnostic search client implementation."""

    def __init__(self) -> None:
        settings = get_settings()
        self.api_key = settings.tavily_api_key
        
        if self.api_key:
            self.client = TavilyClient(api_key=self.api_key)
        else:
            logger.warning("TAVILY_API_KEY not set. SearchClient will use mock results.")
            self.client = None

    def search(self, query: str, max_results: int = 5) -> list[SourceDocument]:
        """Search for documents relevant to a query."""
        
        if not self.client:
            # Mock implementation for baseline testing when no API key is available
            return [
                SourceDocument(
                    title=f"Mock result for: {query}",
                    content=f"This is a mock research result for the query '{query}'. Please provide a Tavily API key to get real results.",
                    url="https://example.com/mock",
                )
            ]

        try:
            results = self.client.search(query=query, max_results=max_results)
            documents = []
            for res in results.get("results", []):
                documents.append(
                    SourceDocument(
                        title=res.get("title", "Untitled"),
                        content=res.get("content", ""),
                        url=res.get("url", ""),
                        metadata={"score": res.get("score")}
                    )
                )
            return documents
        except Exception as e:
            logger.error(f"Tavily search failed: {e}")
            return []
