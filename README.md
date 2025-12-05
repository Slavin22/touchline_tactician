# Touchline Tactician

An AI agent built with [Agno](https://agno-v2.mintlify.app/) - a framework for building and deploying AI agents, multi-agent teams, and agentic workflows.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your API keys (if needed):
```bash
export ANTHROPIC_API_KEY=your_api_key_here
```

## Usage

Run the agent:
```bash
python main.py
```

Or use the agent programmatically:
```python
from main import create_agent

agent = create_agent()
response = agent.run("Your query here")
print(response.content)
```

## Features

- **Agent Development**: Built with Agno's agent framework
- **Reasoning Tools**: Equipped with reasoning capabilities
- **Web Search**: Can search the web and fetch news using DuckDuckGo
- **Markdown Support**: Responses formatted in markdown

## Resources

- [Agno Documentation](https://agno-v2.mintlify.app/)
- [Agno GitHub](https://github.com/agno-agi/agno)

