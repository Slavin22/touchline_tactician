"""Orchestrator Agent - Coordinates the tactical planning workflow."""
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.team import Team
from agno.tools.reasoning import ReasoningTools

from .editor import create_editor_agent
from .plan_builder import create_plan_builder_agent
from .report_generator import create_report_generator_agent
from .visualizer import create_visualizer_agent


def create_orchestrator_team(plans_directory: str = "storage/plans", reports_directory: str = "storage/reports") -> Team:
    """
    Create the Orchestrator Team that coordinates all agents.
    
    Args:
        plans_directory: Directory where plans are stored
        reports_directory: Directory where reports are saved
    
    Returns:
        Configured Team with all agents
    """
    # Create individual agents
    plan_builder = create_plan_builder_agent(plans_directory=plans_directory)
    visualizer = create_visualizer_agent(plans_directory=plans_directory)
    editor = create_editor_agent(plans_directory=plans_directory)
    report_generator = create_report_generator_agent(
        plans_directory=plans_directory,
        output_directory=reports_directory,
    )
    
    # Create orchestrator agent
    orchestrator = Agent(
        name="Orchestrator",
        role="Coordinator",
        model=Claude(id="claude-sonnet-4-20250514"),
        tools=[
            ReasoningTools(add_instructions=True),
        ],
        instructions="""
        You are the orchestrator for the Touchline Tactician system. You coordinate
        a team of specialized agents to help soccer coaches create, visualize, edit,
        and document tactical plans.
        
        Your team members are:
        1. **PlanBuilder** - Creates tactical plans from structured inputs
        2. **Visualizer** - Generates ASCII tactical board diagrams
        3. **Editor** - Modifies existing tactical plans based on commands
        4. **ReportGenerator** - Creates markdown reports (executive, coach, player)
        
        When a user makes a request:
        1. Determine which agent(s) should handle the request
        2. Delegate the task to the appropriate agent(s)
        3. Coordinate multi-step workflows (e.g., create plan then visualize)
        4. Return clear, helpful responses to the user
        
        Common user requests:
        - "Create a new tactical plan" → Delegate to PlanBuilder
        - "Show me the board for plan X" → Delegate to Visualizer
        - "Edit plan X: move player 10 to LW" → Delegate to Editor
        - "Generate reports for plan X" → Delegate to ReportGenerator
        - "Create a plan and show the board" → Delegate to PlanBuilder, then Visualizer
        
        Always be helpful and guide users through the tactical planning process.
        """,
        markdown=True,
    )
    
    # Create the team
    team = Team(
        name="TouchlineTactician",
        members=[
            orchestrator,
            plan_builder,
            visualizer,
            editor,
            report_generator,
        ],
        model=Claude(id="claude-sonnet-4-20250514"),
        instructions="""
        You are the Touchline Tactician team, helping soccer coaches create and manage
        tactical plans. Work together to provide the best possible assistance.
        """,
        markdown=True,
    )
    
    return team

