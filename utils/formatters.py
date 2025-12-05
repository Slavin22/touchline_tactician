"""Markdown formatting utilities."""
from typing import Dict

from models.tactical_plan import TacticalPlan


def format_markdown_report(content: str, title: str = "", level: int = 1) -> str:
    """
    Format content as markdown with proper headers.
    
    Args:
        content: The content to format
        title: Optional title for the report
        level: Header level (1-6)
    
    Returns:
        Formatted markdown string
    """
    lines = []
    
    if title:
        header_char = "#" * level
        lines.append(f"{header_char} {title}")
        lines.append("")
    
    lines.append(content)
    
    return "\n".join(lines)

