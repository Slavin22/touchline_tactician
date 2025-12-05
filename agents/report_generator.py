"""Report Generator Agent - Creates markdown reports from tactical plans."""
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.reasoning import ReasoningTools
from agno.tools.file_generation import FileGenerationTools

from tools.file_operations import TacticalPlanFileTools


def create_report_generator_agent(plans_directory: str = "storage/plans", output_directory: str = "storage/reports") -> Agent:
    """
    Create the Report Generator Agent.
    
    This agent generates three types of reports:
    - Executive summary (1 page)
    - Coach report (5-10 pages)
    - Player-specific reports (2-3 pages each)
    
    Args:
        plans_directory: Directory where plans are stored
        output_directory: Directory where reports are saved
    
    Returns:
        Configured Report Generator Agent
    """
    agent = Agent(
        name="ReportGenerator",
        role="Documentation Specialist",
        model=Claude(id="claude-sonnet-4-20250514"),
        tools=[
            ReasoningTools(add_instructions=True),
            TacticalPlanFileTools(plans_directory=plans_directory),
            FileGenerationTools(
                enable_txt_generation=True,
                output_directory=output_directory,
            ),
        ],
        instructions="""
        You are a tactical report generator. Your role is to create comprehensive
        markdown reports from tactical plans.
        
        You generate three types of reports:
        
        1. **Executive Summary** (1 page):
           - High-level strategy overview
           - Key formation and tactics
           - Main tactical principles
           - Suitable for team executives
        
        2. **Coach Report** (5-10 pages):
           - Detailed tactical analysis
           - All game phases (attack, defense, transition)
           - Player roles and responsibilities
           - Pressing triggers and instructions
           - Set piece strategies
           - Comprehensive tactical breakdown
        
        3. **Player-Specific Reports** (2-3 pages each):
           - Detailed view of the player's zone
           - Personal responsibilities in all phases
           - Movement patterns and key actions
           - High-level overview of rest of field
           - Phase-specific instructions (attack/defense/transition)
        
        When generating reports:
        1. Load the plan using load_plan
        2. Generate the appropriate report content based on the request
        3. Use markdown formatting for structure
        4. Save the report using the file generation tools
        5. Return the file path and summary
        
        Use clear headings, bullet points, and structured sections.
        Make the reports professional and easy to read.
        """,
        markdown=True,
    )
    return agent

