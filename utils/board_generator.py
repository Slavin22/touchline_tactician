"""ASCII tactical board generator."""
from typing import List

from models.tactical_plan import Player, TacticalPlan


def generate_ascii_board(plan: TacticalPlan, width: int = 80, height: int = 30) -> str:
    """
    Generate an ASCII representation of the tactical board.
    
    Args:
        plan: The tactical plan to visualize
        width: Width of the board in characters
        height: Height of the board in characters
    
    Returns:
        ASCII string representation of the tactical board
    """
    # Create a grid to represent the field
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    
    # Draw field boundaries
    for i in range(height):
        grid[i][0] = '|'
        grid[i][width-1] = '|'
    
    for j in range(width):
        grid[0][j] = '-'
        grid[height-1][j] = '-'
    
    # Draw center line
    center_x = width // 2
    for i in range(1, height-1):
        grid[i][center_x] = '|'
    
    # Draw center circle (simplified)
    center_y = height // 2
    circle_radius = min(width, height) // 8
    
    # Place players on the field
    player_positions = []
    for player in plan.players:
        # Convert zone coordinates to grid coordinates
        # Field is 0-100, grid is 0-width/height
        zone = player.zone
        x = int((zone.x_min + zone.x_max) / 2 * width / 100)
        y = int((zone.y_min + zone.y_max) / 2 * height / 100)
        
        # Clamp to grid bounds
        x = max(1, min(width-2, x))
        y = max(1, min(height-2, y))
        
        # Place player number
        player_num_str = str(player.number)
        if len(player_num_str) == 1:
            grid[y][x] = player_num_str
        else:
            # Two-digit number
            if x < width - 1:
                grid[y][x] = player_num_str[0]
                grid[y][x+1] = player_num_str[1]
        
        player_positions.append({
            'number': player.number,
            'position': player.position,
            'x': x,
            'y': y
        })
    
    # Build the output string
    lines = []
    lines.append(f"Formation: {plan.formation}")
    lines.append(f"Plan: {plan.name}")
    lines.append("")
    lines.append(" " + "".join(grid[0]))
    
    for row in grid[1:-1]:
        lines.append(" " + "".join(row))
    
    lines.append(" " + "".join(grid[-1]))
    lines.append("")
    
    # Add player legend
    lines.append("Players:")
    for pos in sorted(player_positions, key=lambda p: p['number']):
        lines.append(f"  {pos['number']:2d}: {pos['position']}")
    
    return "\n".join(lines)

