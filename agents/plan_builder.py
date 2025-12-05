"""Plan Builder Agent - Creates tactical plans from structured inputs."""
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.reasoning import ReasoningTools

from models.tactical_plan import TacticalPlan
from tools.file_operations import TacticalPlanFileTools
from tools.tactical_validator import TacticalValidatorTools


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
    agent = Agent(
        name="PlanBuilder",
        role="Tactical Specialist",
        model=Claude(id="claude-sonnet-4-20250514"),
        tools=[
            ReasoningTools(add_instructions=True),
            TacticalPlanFileTools(plans_directory=plans_directory),
            TacticalValidatorTools(),
        ],
        instructions="""
        You are a tactical planning specialist for soccer. Your role is to create detailed
        tactical plans based on structured inputs from coaches.
        
        When creating a tactical plan, you should:
        1. Ask for or extract the following information:
           - Plan name
           - Formation (e.g., 4-3-3, 4-4-2)
           - Player positions and numbers
           - Player zones on the field
           - Player responsibilities
           - Phase-specific instructions (attack, defense, transition)
           - Pressing triggers
           - Transition instructions
        
        2. Create a TacticalPlan object with all the information
        
        3. Validate the plan using the validation tools:
           - validate_formation: Check formation is correct
           - validate_player_positions: Check positions are valid
           - validate_zones: Check zones are properly defined
           - check_tactical_consistency: Check overall consistency
        
        4. If validation passes, save the plan using save_plan
        
        5. Return the plan_id and confirmation that the plan was created
        
        Be thorough and ensure all tactical details are captured accurately.
        """,
        markdown=True,
    )
    return agent

