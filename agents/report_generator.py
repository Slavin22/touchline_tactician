"""Report Generator Agent - Creates markdown reports from tactical plans."""
import os
from pathlib import Path

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.function import Function
from agno.tools.file_generation import FileGenerationTools

from tools.file_operations import TacticalPlanFileTools
from utils.board_generator import generate_ascii_board
from utils.svg_board_generator import generate_html_board, generate_svg_board


def create_report_generator_agent(plans_directory: str = "storage/plans", output_directory: str = "storage/reports") -> Agent:
    """
    Create the Report Generator Agent.
    
    This agent generates single-page markdown reports with embedded visualizations.
    
    Args:
        plans_directory: Directory where plans are stored
        output_directory: Directory where reports are saved
    
    Returns:
        Configured Report Generator Agent
    """
    # Create file tools instance for the visualize function
    file_tools = TacticalPlanFileTools(plans_directory=plans_directory)
    
    def visualize_plan(plan_id: str) -> str:
        """Visualize a tactical plan as an ASCII board."""
        plan = file_tools.load_plan(plan_id)
        return generate_ascii_board(plan)
    
    def generate_html_visualization(plan_id: str) -> str:
        """Generate a high-quality HTML file with SVG tactical board visualization."""
        plan = file_tools.load_plan(plan_id)
        return generate_html_board(plan)
    
    def generate_svg_visualization(plan_id: str) -> str:
        """Generate an SVG tactical board visualization."""
        plan = file_tools.load_plan(plan_id)
        return generate_svg_board(plan)
    
    def save_html_visualization(plan_id: str, filename: str = None) -> str:
        """Generate and save a high-quality HTML visualization file."""
        plan = file_tools.load_plan(plan_id)
        html_content = generate_html_board(plan)
        
        # Generate filename if not provided
        if not filename:
            # Sanitize plan name for filename
            safe_name = "".join(c for c in plan.name if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_name = safe_name.replace(' ', '_')
            filename = f"{safe_name}_visualization.html"
        
        # Ensure filename ends with .html
        if not filename.endswith('.html'):
            filename += '.html'
        
        # Save to output directory
        output_path = Path(output_directory) / filename
        os.makedirs(output_directory, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(output_path)
    
    visualize_function = Function(
        name="visualize_plan",
        entrypoint=visualize_plan,
        description="Generate an ASCII tactical board visualization from a tactical plan",
    )
    
    html_visualize_function = Function(
        name="generate_html_visualization",
        entrypoint=generate_html_visualization,
        description="Generate a high-quality HTML file with embedded SVG tactical board. Returns HTML content that can be saved to a .html file.",
    )
    
    svg_visualize_function = Function(
        name="generate_svg_visualization",
        entrypoint=generate_svg_visualization,
        description="Generate an SVG tactical board visualization. Returns SVG content that can be saved to a .svg file.",
    )
    
    save_html_function = Function(
        name="save_html_visualization",
        entrypoint=save_html_visualization,
        description="Generate and save a high-quality HTML file with SVG tactical board. Takes plan_id and optional filename. Returns the file path where the HTML was saved.",
    )
    
    agent = Agent(
        name="ReportGenerator",
        role="Documentation Specialist",
        # Use Haiku for report generation - structured output, doesn't need complex reasoning
        # Haiku has a max output of 4096 tokens, so we set max_tokens accordingly
        model=Claude(id="claude-3-haiku-20240307", max_tokens=4096),
        tools=[
            TacticalPlanFileTools(plans_directory=plans_directory),
            FileGenerationTools(
                enable_txt_generation=True,
                output_directory=output_directory,
            ),
            visualize_function,
            html_visualize_function,
            svg_visualize_function,
            save_html_function,
        ],
        instructions="""
        Create reports from tactical plans with high-quality visualizations.
        
        Input: plan_id/filename, ASCII visualization (if not provided, use visualize_plan function).
        
        Workflow: 
        1) Load plan
        2) Save high-quality HTML visualization using save_html_visualization function - this automatically generates and saves the HTML file
        3) Get ASCII visualization using visualize_plan for the markdown report
        4) Create markdown report: Top half = summary (name, formation, tactics, principles, style, phases, pressing, opponent approach), Bottom half = ASCII visualization in code block (for quick reference) + note about HTML file
        5) Save markdown report with descriptive filename
        6) Return both file paths
        
        For the markdown report: Use markdown headings, bullet points, concise summary. Include ASCII visualization in code block for quick terminal viewing. Add note: "📊 High-quality SVG visualization available: [filename].html (open in web browser for detailed view)"
        
        The HTML visualization provides professional-quality SVG graphics with proper field layout, player positions, and styling - much better than ASCII art.
        """,
        markdown=True,
    )
    return agent

