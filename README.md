# Touchline Tactician

A multi-agent AI application that helps soccer coaches create, visualize, edit, and document tactical plans using the Agno framework.

## Features

- **Multi-Agent Architecture**: Coordinated team of specialized AI agents
- **Tactical Plan Creation**: Build detailed tactical plans with formations, player positions, zones, and phase-specific instructions
- **ASCII Visualization**: Generate tactical board diagrams in the terminal
- **Plan Editing**: Modify existing plans with natural language commands
- **Report Generation**: Create three types of reports:
  - Executive Summary (1 page) - For team executives
  - Coach Report (5-10 pages) - Detailed tactical analysis
  - Player Reports (2-3 pages each) - Individual player instructions

## Architecture

The system uses a multi-agent team structure:

1. **Orchestrator Agent** - Coordinates workflow and routes requests
2. **Plan Builder Agent** - Creates tactical plans from structured inputs
3. **Visualization Agent** - Generates ASCII tactical board diagrams
4. **Editor Agent** - Modifies existing tactical plans
5. **Report Generator Agent** - Creates markdown reports

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your API keys:
```bash
export ANTHROPIC_API_KEY=your_api_key_here
```

## Usage

Run the CLI application:
```bash
python main.py
```

### Available Commands

- `create` - Create a new tactical plan
- `visualize <plan_id>` - Show ASCII tactical board for a plan
- `edit <plan_id> <command>` - Edit an existing tactical plan
- `generate <type> <plan_id>` - Generate reports (executive, coach, or player)
- `list` - List all saved tactical plans
- `help` - Show help message
- `exit` or `quit` - Exit the application

### Examples

```
Touchline Tactician> create
Touchline Tactician> visualize plan_123.json
Touchline Tactician> edit plan_123.json move player 10 to LW
Touchline Tactician> generate executive plan_123.json
Touchline Tactician> generate coach plan_123.json
Touchline Tactician> generate player 10 plan_123.json
Touchline Tactician> list
```

## Project Structure

```
touchline_tactician/
├── main.py                 # CLI entry point
├── agents/
│   ├── orchestrator.py    # Orchestrator Agent
│   ├── plan_builder.py    # Plan Builder Agent
│   ├── visualizer.py      # Visualization Agent
│   ├── editor.py          # Editor Agent
│   └── report_generator.py # Report Generator Agent
├── models/
│   └── tactical_plan.py   # Data models (Pydantic)
├── tools/
│   ├── file_operations.py # File storage tools
│   └── tactical_validator.py # Validation tools
├── storage/
│   ├── plans/             # JSON plan files
│   └── reports/          # Generated reports
└── utils/
    ├── board_generator.py # ASCII board generation
    └── formatters.py     # Markdown formatting
```

## Tactical Plan Structure

Plans are stored as JSON files with the following structure:

- **Formation**: Standard formations (4-3-3, 4-4-2, etc.)
- **Players**: List of players with positions, zones, and responsibilities
- **Zones**: Field zones for each player
- **Phases**: Attack, defense, and transition instructions
- **Pressing Triggers**: Conditions for pressing
- **Transition Instructions**: Attack-to-defense and defense-to-attack instructions

## User Guide

See `USER_GUIDE.md` for detailed usage instructions, example prompts, and best practices.

## Development Roadmap

See `touchline-tactician-roadmap.plan.md` for the complete development plan and progress tracking.

## Resources

- [Agno Documentation](https://agno-v2.mintlify.app/)
- [Agno GitHub](https://github.com/agno-agi/agno)
