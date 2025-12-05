"""Editor Agent - Modifies tactical plans based on commands."""
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.reasoning import ReasoningTools

from tools.file_operations import TacticalPlanFileTools
from tools.tactical_validator import TacticalValidatorTools


def create_editor_agent(plans_directory: str = "storage/plans") -> Agent:
    """
    Create the Editor Agent.
    
    This agent processes edit commands and modifies tactical plans.
    
    Args:
        plans_directory: Directory where plans are stored
    
    Returns:
        Configured Editor Agent
    """
    agent = Agent(
        name="Editor",
        role="Plan Modifier",
        model=Claude(id="claude-sonnet-4-20250514"),
        tools=[
            ReasoningTools(add_instructions=True),
            TacticalPlanFileTools(plans_directory=plans_directory),
            TacticalValidatorTools(),
        ],
        instructions="""
        You are a tactical plan editor. Your role is to modify existing tactical plans
        based on edit commands from coaches.
        
        Common edit commands include:
        - "move player X to [position]" - Move a player to a new position
        - "change formation to X-Y-Z" - Change the formation
        - "update player X zone to ..." - Update a player's zone
        - "add pressing trigger ..." - Add a pressing trigger
        - "update player X responsibilities ..." - Update player responsibilities
        
        When processing an edit:
        1. Load the plan using load_plan
        2. Parse the edit command to understand what needs to change
        3. Make the appropriate modifications to the plan object
        4. Validate the changes using the validation tools
        5. If valid, save the updated plan using save_plan
        6. Return confirmation of the changes
        
        Always validate changes before saving. If validation fails, explain why
        and suggest alternatives.
        """,
        markdown=True,
    )
    return agent

