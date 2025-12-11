"""Visualization Agent - Generates ASCII tactical board diagrams."""
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.function import Function

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
        # Use Haiku for simple visualization task - much cheaper than Sonnet 4
        # Haiku has a max output of 4096 tokens, so we set max_tokens accordingly
        model=Claude(id="claude-3-haiku-20240307", max_tokens=4096),
        tools=[
            TacticalPlanFileTools(plans_directory=plans_directory),
            visualize_function,
        ],
        instructions="""
        Generate ASCII tactical board visualizations. 
        
        When asked to visualize a plan:
        1. Use the visualize_plan function with the plan_id/filename
        2. The function returns raw ASCII art - output it EXACTLY as returned
        3. Do NOT describe, interpret, or summarize the visualization
        4. Output the complete ASCII art string directly so it displays properly in the terminal
        
        The ASCII output includes the field, player positions, and legend - output it verbatim.
        """,
        markdown=True,
    )
    
    return agent

