"""Plan Builder Agent - Creates tactical plans from structured inputs."""
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.function import Function
from agno.tools.reasoning import ReasoningTools

from models.tactical_plan import TacticalPlan
from tools.file_operations import TacticalPlanFileTools
from tools.tactical_validator import TacticalValidatorTools
from utils.board_generator import generate_ascii_board


def create_plan_builder_agent(plans_directory: str = "storage/plans") -> Agent:
    """
    Create the Plan Builder Agent.
    
    This agent creates tactical plans from structured inputs, validates them,
    and saves them to storage.
    
    Args:
        plans_directory: Directory where plans are stored
    
    Returns:
        Configured Plan Builder Agent
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
        name="PlanBuilder",
        role="Tactical Specialist",
        model=Claude(id="claude-sonnet-4-20250514"),
        tools=[
            ReasoningTools(add_instructions=True),
            TacticalPlanFileTools(plans_directory=plans_directory),
            TacticalValidatorTools(plans_directory=plans_directory),
            visualize_function,
        ],
        instructions="""
        Create tactical plans from team/opponent info.
        
        Input: Plan name, team info (name, formation, style, key players, strengths, weaknesses), opponent info (same fields).
        
        Workflow:
        1. Analyze: Review info, determine approach based on team strengths, opponent weaknesses/strengths, formation matchups.
        2. Build: Create plan with specified formation. CRITICAL: You MUST include exactly 11 players (1 goalkeeper + 10 outfield players) in the players array. Each player must have:
           - number: jersey number (1-99)
           - position: position code (GK, CB, LB, RB, CDM, CM, CAM, LW, RW, ST, etc.)
           - zone: object with x_min, x_max, y_min, y_max (all 0-100 coordinates)
           - phases: object with attack, defense, and transition phase instructions
        Use create_plan tool with complete plan_data dict containing all 11 players.
        3. Validate: After creating a plan, use load_plan to get the plan object, then pass that plan object (not just the plan_id) to validation tools. The validation will check that you have exactly 11 players. Fix any issues if needed.
        4. Return: Brief description (team names, formation, tactics, pressing, transitions, how it exploits opponent), plan_id. No visualization.
        
        CRITICAL REQUIREMENTS:
        - Exactly 11 players (1 GK + 10 outfield) - NO EXCEPTIONS
        - All players must have zones with valid coordinates (0-100)
        - All players must have phase instructions (attack, defense, transition)
        - Save immediately after creation
        - Validate after saving to ensure all 11 players are present
        
        IMPORTANT: When validating, use load_plan to get the full plan object and pass that to validation tools, not just the plan_id string.
        """,
        markdown=True,
    )
    return agent

