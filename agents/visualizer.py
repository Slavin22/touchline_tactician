"""Visualization Agent - Generates ASCII tactical board diagrams."""
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.function import Function
from agno.tools.reasoning import ReasoningTools

from tools.file_operations import TacticalPlanFileTools
from utils.board_generator import generate_ascii_board


def create_visualizer_agent(plans_directory: str = "storage/plans") -> Agent:
    """
    Create the Visualization Agent.
    
    This agent generates ASCII tactical board diagrams from tactical plans.
    
    Args:
        plans_directory: Directory where plans are stored
    
    Returns:
        Configured Visualization Agent
    """
    # Create file tools instance for the visualize function
    file_tools = TacticalPlanFileTools(plans_directory=plans_directory)
    
    def visualize_plan(plan_id: str) -> str:
        """
        Visualize a tactical plan as an ASCII board.
        
        Args:
            plan_id: The plan ID or filename (with or without .json extension)
        
        Returns:
            ASCII representation of the tactical board
        """
        plan = file_tools.load_plan(plan_id)
        return generate_ascii_board(plan)
    
    visualize_function = Function(
        name="visualize_plan",
        entrypoint=visualize_plan,
        description="Generate an ASCII tactical board visualization from a tactical plan",
    )
    
    agent = Agent(
        name="Visualizer",
        role="Board Generator",
        model=Claude(id="claude-sonnet-4-20250514"),
        tools=[
            ReasoningTools(add_instructions=True),
            TacticalPlanFileTools(plans_directory=plans_directory),
            visualize_function,
        ],
        instructions="""
        You are a tactical board visualization specialist. Your role is to generate
        ASCII representations of tactical plans.
        
        When asked to visualize a plan:
        1. Use the visualize_plan function with the plan filename or plan_id
        2. The function will load the plan and generate the ASCII board
        3. Display the result to the user
        
        The ASCII board shows:
        - Field boundaries
        - Player positions (by number)
        - Formation lines
        - Player legend
        
        Always display the board clearly and include the plan name and formation.
        """,
        markdown=True,
    )
    
    return agent

