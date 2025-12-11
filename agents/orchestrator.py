"""Orchestrator Agent - Coordinates the tactical planning workflow."""
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.team import Team

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
        # Use Haiku for coordination - mostly routing tasks, doesn't need Sonnet 4's capabilities
        # Haiku has a max output of 4096 tokens, so we set max_tokens accordingly
        model=Claude(id="claude-3-haiku-20240307", max_tokens=4096),
        instructions="""
        You coordinate specialized agents for tactical planning.
        
        Team capabilities:
        - PlanBuilder: Creates tactical plans
        - Visualizer: ASCII art visualizations only (visualize_plan function)
        - Editor: Modifies existing plans
        - ReportGenerator: HTML/SVG visualizations (generate_html_visualization, save_html_visualization) AND markdown reports
        
        NEW PLAN WORKFLOW:
        1. Interview: Ask all 13 questions at once (plan name, team name, formation, style, key players, strengths, weaknesses ×2 for both teams). Wait for all answers.
        2. Build: Extract info, delegate to PlanBuilder with structured data.
        3. Present: Show plan description (formation, tactics, pressing, transitions), ask for feedback.
        4. Feedback: If changes → Editor → present again. If confirmed → proceed.
        5. Visualize: Delegate to Visualizer for ASCII board, or ReportGenerator for HTML/SVG visualizations.
        6. Report: Delegate to ReportGenerator with plan_id and visualization.
        
        ROUTING RULES:
        - ASCII visualization requests → Visualizer agent
        - HTML/SVG visualization requests → ReportGenerator agent (has generate_html_visualization, save_html_visualization functions)
        - Edit instructions → Editor agent
        - Generate report → ReportGenerator agent
        - Create new plan → PlanBuilder agent
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
        # Use Haiku for team coordination - just routing between agents
        # Haiku has a max output of 4096 tokens, so we set max_tokens accordingly
        model=Claude(id="claude-3-haiku-20240307", max_tokens=4096),
        instructions="""
        You are the Touchline Tactician team, helping soccer coaches create and manage
        tactical plans. Work together to provide the best possible assistance.
        
        Agent capabilities:
        - Visualizer: ASCII art visualizations only
        - ReportGenerator: HTML/SVG visualizations and markdown reports
        - PlanBuilder: Creates new tactical plans
        - Editor: Modifies existing plans
        """,
        markdown=True,
    )
    
    return team

