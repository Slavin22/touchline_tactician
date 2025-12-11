"""Editor Agent - Modifies tactical plans based on commands."""
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.function import Function
from agno.tools.reasoning import ReasoningTools

from tools.file_operations import TacticalPlanFileTools
from tools.tactical_validator import TacticalValidatorTools
from utils.board_generator import generate_ascii_board


def create_editor_agent(plans_directory: str = "storage/plans") -> Agent:
    """
    Create the Editor Agent.
    
    This agent processes edit commands and modifies tactical plans.
    
    Args:
        plans_directory: Directory where plans are stored
    
    Returns:
        Configured Editor Agent
    """
    # Create file tools instance for the visualize function
    file_tools = TacticalPlanFileTools(plans_directory=plans_directory)
    
    def visualize_plan(plan_id: str) -> str:
        """Visualize a tactical plan as an ASCII board."""
        plan = file_tools.load_plan(plan_id)
        return generate_ascii_board(plan)
    
    visualize_function = Function(
        name="visualize_plan",
        entrypoint=visualize_plan,
        description="Generate an ASCII tactical board visualization from a tactical plan",
    )
    
    agent = Agent(
        name="Editor",
        role="Plan Modifier",
        model=Claude(id="claude-sonnet-4-20250514"),
        tools=[
            ReasoningTools(add_instructions=True),
            TacticalPlanFileTools(plans_directory=plans_directory),
            TacticalValidatorTools(plans_directory=plans_directory),
            visualize_function,
        ],
        instructions="""
        Modify tactical plans from free-text instructions (e.g., "move player 10 to left wing", "change formation to 4-4-2").
        
        Process: 1) Find plan (use provided ID, or list_plans for most recent, or ask if unclear), 2) Load plan, 3) Parse ALL changes, 4) Implement together, 5) Validate, 6) Save if valid, 7) Return summary + visualization.
        
        Always: Process all changes together, save automatically, show updated board, ask for clarification if ambiguous.
        """,
        markdown=True,
    )
    return agent

