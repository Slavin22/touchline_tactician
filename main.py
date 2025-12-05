"""
Touchline Tactician - AI Agent using Agno
"""
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.reasoning import ReasoningTools
from agno.tools.duckduckgo import DuckDuckGoTools


def create_agent():
    """Create and configure the Agno agent."""
    agent = Agent(
        model=Claude(id="claude-sonnet-4-20250514"),
        tools=[
            ReasoningTools(add_instructions=True),
            DuckDuckGoTools(search=True, news=True),
        ],
        instructions="You are a helpful AI assistant. Use tables to display data when appropriate.",
        markdown=True,
    )
    return agent


def main():
    """Main entry point for the application."""
    agent = create_agent()
    
    # Example: Run the agent with a query
    response = agent.run("Hello! What can you help me with?")
    print(response.content)


if __name__ == "__main__":
    main()

