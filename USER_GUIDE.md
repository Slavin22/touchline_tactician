# Touchline Tactician - User Guide

## Overview

Touchline Tactician is an AI-powered tactical planning assistant for soccer coaches. It helps you create, visualize, edit, and document tactical plans using a team of specialized AI agents. The system understands soccer tactics and can help you build comprehensive tactical plans with formations, player positions, zones, and phase-specific instructions.

## Getting Started

### Prerequisites

1. **API Key**: You'll need an Anthropic API key to use the application
   ```bash
   export ANTHROPIC_API_KEY=your_api_key_here
   ```

2. **Virtual Environment**: Activate the virtual environment
   ```bash
   source tt_env/bin/activate
   ```

### Launching the Application

Run the CLI application:
```bash
python main.py
```

You'll see the Touchline Tactician banner and a command prompt:
```
Touchline Tactician> 
```

## How to Use the Application

### Basic Workflow

1. **Create a Tactical Plan** - Start by creating a new tactical plan
2. **Visualize the Plan** - View the tactical board as an ASCII diagram
3. **Edit the Plan** - Make adjustments using natural language commands
4. **Generate Reports** - Create executive, coach, or player-specific reports

### Available Commands

- `create` - Create a new tactical plan
- `visualize <plan_id>` - Show ASCII tactical board for a plan
- `edit <plan_id> <command>` - Edit an existing tactical plan
- `generate <type> <plan_id>` - Generate reports (executive, coach, or player)
- `list` - List all saved tactical plans
- `help` - Show help message
- `exit` or `quit` - Exit the application

## Example Prompts

### Creating a Tactical Plan

The system will guide you through creating a tactical plan with structured prompts. Here are some example interactions:

#### Example 1: Create a 4-3-3 Formation

```
Touchline Tactician> create

I'll help you create a new tactical plan. Let me gather the necessary information.

Plan name: High Press 4-3-3
Formation: 4-3-3
```

The system will then prompt you for:
- Player positions and numbers
- Player zones on the field
- Player responsibilities
- Phase-specific instructions (attack, defense, transition)
- Pressing triggers
- Transition instructions

#### Example 2: Create a Defensive 4-4-2

```
Touchline Tactician> create a defensive 4-4-2 formation with deep block

I'll create a defensive 4-4-2 tactical plan with a deep defensive block.
```

#### Example 3: Create a Counter-Attacking 3-5-2

```
Touchline Tactician> create a counter-attacking 3-5-2 formation with wing backs

I'll help you build a counter-attacking 3-5-2 system with attacking wing backs.
```

### Visualizing Tactical Plans

Once you have a plan, you can visualize it as an ASCII tactical board:

#### Example 1: Visualize by Plan ID

```
Touchline Tactician> visualize plan_abc123.json
```

#### Example 2: Visualize Latest Plan

```
Touchline Tactician> show me the board for my latest plan
```

#### Example 3: Visualize with Specific Plan Name

```
Touchline Tactician> visualize "High Press 4-3-3"
```

### Editing Tactical Plans

You can modify existing plans using natural language commands:

#### Example 1: Move a Player

```
Touchline Tactician> edit plan_abc123.json move player 10 to left wing
```

#### Example 2: Change Formation

```
Touchline Tactician> edit plan_abc123.json change formation to 4-2-3-1
```

#### Example 3: Update Player Zone

```
Touchline Tactician> edit plan_abc123.json update player 7 zone to cover the right flank
```

#### Example 4: Add Pressing Trigger

```
Touchline Tactician> edit plan_abc123.json add pressing trigger when opponent plays back pass
```

#### Example 5: Update Player Responsibilities

```
Touchline Tactician> edit plan_abc123.json update player 9 responsibilities to press high and cut passing lanes
```

#### Example 6: Modify Transition Instructions

```
Touchline Tactician> edit plan_abc123.json update transition instructions for quick counter when we win the ball
```

### Generating Reports

The system can generate three types of reports:

#### Executive Summary (1 page)

```
Touchline Tactician> generate executive plan_abc123.json
```

This creates a high-level summary suitable for team executives, covering:
- Overall strategy
- Key formation and tactics
- Main tactical principles

#### Coach Report (5-10 pages)

```
Touchline Tactician> generate coach plan_abc123.json
```

This creates a detailed tactical analysis including:
- Complete tactical breakdown
- All game phases (attack, defense, transition)
- Player roles and responsibilities
- Pressing triggers and instructions
- Set piece strategies

#### Player-Specific Reports (2-3 pages each)

```
Touchline Tactician> generate player 10 plan_abc123.json
```

This creates an individual report for a specific player covering:
- Detailed view of the player's zone
- Personal responsibilities in all phases
- Movement patterns and key actions
- High-level overview of rest of field
- Phase-specific instructions (attack/defense/transition)

#### Generate All Reports

```
Touchline Tactician> generate all reports for plan_abc123.json
```

### Listing Plans

View all your saved tactical plans:

```
Touchline Tactician> list
```

This will show all available plan files in the storage directory.

### Complex Workflows

#### Example 1: Create and Immediately Visualize

```
Touchline Tactician> create a 4-3-3 formation and show me the board
```

#### Example 2: Create, Edit, and Generate Reports

```
Touchline Tactician> create a 4-4-2 formation
[Plan created: plan_xyz789.json]

Touchline Tactician> edit plan_xyz789.json move player 11 to striker position
[Plan updated]

Touchline Tactician> generate coach plan_xyz789.json
[Coach report generated]

Touchline Tactician> generate player 11 plan_xyz789.json
[Player report generated]
```

#### Example 3: Quick Plan Modification

```
Touchline Tactician> edit plan_abc123.json change to high press and move midfielders forward
```

## Understanding the Output

### Tactical Board Visualization

The ASCII board shows:
- Field boundaries (top, bottom, sides)
- Center line dividing the field
- Player positions marked by jersey numbers
- Formation structure
- Player legend showing numbers and positions

### Plan Files

Plans are saved as JSON files in `storage/plans/` with the following structure:
- Plan metadata (name, ID, timestamps)
- Formation information
- Player details (positions, zones, responsibilities)
- Phase-specific instructions
- Pressing triggers
- Transition instructions

### Reports

Reports are saved as markdown files in `storage/reports/` and can be:
- Viewed in any markdown viewer
- Converted to PDF or other formats
- Shared with team members
- Printed for team meetings

## Tips for Best Results

1. **Be Specific**: When creating plans, provide as much detail as possible about your tactical intentions
2. **Use Standard Terminology**: The system understands common soccer terms (formations, positions, tactics)
3. **Iterate**: Start with a basic plan, then use edit commands to refine it
4. **Validate**: The system automatically validates plans for consistency
5. **Save Often**: Plans are automatically saved, but you can create multiple versions

## Common Use Cases

### Pre-Match Planning

1. Create a tactical plan for the upcoming match
2. Visualize the formation and player positions
3. Generate coach report for your analysis
4. Generate player reports for individual briefings

### In-Season Adjustments

1. Load an existing plan
2. Edit to reflect new tactics or player changes
3. Generate updated reports
4. Share with team

### Training Session Planning

1. Create a plan focused on specific training scenarios
2. Visualize the setup
3. Generate player reports for training instructions

## Troubleshooting

### Plan Not Found

If you get a "plan not found" error:
- Use `list` to see all available plans
- Check that you're using the correct plan ID or filename
- Ensure the plan file exists in `storage/plans/`

### Validation Errors

If a plan fails validation:
- The system will explain what's wrong
- Common issues: missing players, invalid positions, zone conflicts
- Use edit commands to fix the issues

### API Errors

If you encounter API errors:
- Check that your `ANTHROPIC_API_KEY` is set correctly
- Verify you have API credits available
- Check your internet connection

## Advanced Features

### Custom Formations

The system supports standard formations (4-3-3, 4-4-2, etc.) and can work with custom formations. Just describe your formation when creating a plan.

### Zone Definitions

Zones are defined using coordinates (0-100) representing the field:
- X-axis: Left (0) to Right (100)
- Y-axis: Defensive (0) to Attacking (100)

### Phase-Specific Instructions

Each player can have different instructions for:
- **Attack**: When in possession
- **Defense**: When out of possession
- **Transition**: When transitioning between phases

## Future Enhancements

As the application evolves, you can expect:
- Web interface for easier interaction
- Interactive visual tactical board
- Natural language input for plan creation
- Advanced tactical analysis
- Plan comparison tools
- Version history and rollback

## Getting Help

- Type `help` in the application for command reference
- Check the README.md for technical details
- Review the roadmap file for planned features

---

**Last Updated**: 2025-01-27
**Version**: 1.0.0 (Initial Implementation)

