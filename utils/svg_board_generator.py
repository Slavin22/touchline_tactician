"""SVG/HTML tactical board generator for high-quality visualizations."""
from models.tactical_plan import TacticalPlan


def generate_svg_board(plan: TacticalPlan, width: int = 800, height: int = 600) -> str:
    """
    Generate an SVG representation of the tactical board.
    
    Args:
        plan: The tactical plan to visualize
        width: Width of the SVG in pixels
        height: Height of the SVG in pixels
    
    Returns:
        SVG string representation of the tactical board
    """
    # Field proportions (soccer field is typically 105m x 68m, but we'll use a standard ratio)
    field_width = width - 40  # Leave margins
    field_height = height - 100  # Leave space for title and legend
    field_x = 20
    field_y = 60
    
    # Calculate player positions
    player_positions = []
    for player in plan.players:
        zone = player.zone
        # Convert zone coordinates (0-100) to SVG coordinates
        x = field_x + (zone.x_min + zone.x_max) / 2 * field_width / 100
        y = field_y + (zone.y_min + zone.y_max) / 2 * field_height / 100
        
        player_positions.append({
            'number': player.number,
            'position': player.position,
            'x': x,
            'y': y
        })
    
    # Build SVG
    svg_lines = [
        f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
        '  <defs>',
        '    <style>',
        '      .field { fill: #2d5016; stroke: #ffffff; stroke-width: 2; }',
        '      .line { stroke: #ffffff; stroke-width: 2; fill: none; }',
        '      .circle { stroke: #ffffff; stroke-width: 2; fill: none; }',
        '      .player-circle { fill: #1a4d00; stroke: #ffffff; stroke-width: 2; }',
        '      .player-text { fill: #ffffff; font-family: Arial, sans-serif; font-weight: bold; font-size: 14px; text-anchor: middle; dominant-baseline: central; }',
        '      .title { fill: #000000; font-family: Arial, sans-serif; font-size: 20px; font-weight: bold; }',
        '      .subtitle { fill: #333333; font-family: Arial, sans-serif; font-size: 14px; }',
        '      .legend-text { fill: #000000; font-family: Arial, sans-serif; font-size: 12px; }',
        '    </style>',
        '  </defs>',
        '',
        '  <!-- Title -->',
        f'  <text x="{width//2}" y="25" class="title" text-anchor="middle">{plan.name}</text>',
        f'  <text x="{width//2}" y="45" class="subtitle" text-anchor="middle">Formation: {plan.formation}</text>',
        '',
        '  <!-- Field -->',
        f'  <rect x="{field_x}" y="{field_y}" width="{field_width}" height="{field_height}" class="field" rx="5"/>',
        '',
        '  <!-- Center line -->',
        f'  <line x1="{field_x + field_width//2}" y1="{field_y}" x2="{field_x + field_width//2}" y2="{field_y + field_height}" class="line"/>',
        '',
        '  <!-- Center circle -->',
        f'  <circle cx="{field_x + field_width//2}" cy="{field_y + field_height//2}" r="{min(field_width, field_height)//8}" class="circle"/>',
        '',
        '  <!-- Penalty boxes (simplified) -->',
        f'  <rect x="{field_x}" y="{field_y + field_height//3}" width="{field_width//6}" height="{field_height//3}" class="line" fill="none"/>',
        f'  <rect x="{field_x + field_width - field_width//6}" y="{field_y + field_height//3}" width="{field_width//6}" height="{field_height//3}" class="line" fill="none"/>',
        '',
        '  <!-- Goal boxes (simplified) -->',
        f'  <rect x="{field_x}" y="{field_y + field_height//2.5}" width="{field_width//12}" height="{field_height//5}" class="line" fill="none"/>',
        f'  <rect x="{field_x + field_width - field_width//12}" y="{field_y + field_height//2.5}" width="{field_width//12}" height="{field_height//5}" class="line" fill="none"/>',
        '',
        '  <!-- Players -->',
    ]
    
    # Add player circles and numbers
    for pos in player_positions:
        svg_lines.append(f'  <circle cx="{pos["x"]}" cy="{pos["y"]}" r="18" class="player-circle"/>')
        svg_lines.append(f'  <text x="{pos["x"]}" y="{pos["y"]}" class="player-text">{pos["number"]}</text>')
    
    # Add legend
    svg_lines.extend([
        '',
        '  <!-- Legend -->',
        f'  <text x="{field_x}" y="{field_y + field_height + 20}" class="legend-text">Players:</text>',
    ])
    
    # Sort players by number for legend
    sorted_players = sorted(player_positions, key=lambda p: p['number'])
    legend_y = field_y + field_height + 35
    legend_x = field_x
    items_per_row = 6
    for i, pos in enumerate(sorted_players):
        if i > 0 and i % items_per_row == 0:
            legend_y += 15
            legend_x = field_x
        svg_lines.append(f'  <text x="{legend_x}" y="{legend_y}" class="legend-text">{pos["number"]}: {pos["position"]}</text>')
        legend_x += 100
    
    svg_lines.append('</svg>')
    
    return '\n'.join(svg_lines)


def generate_html_board(plan: TacticalPlan, width: int = 800, height: int = 600) -> str:
    """
    Generate a complete HTML page with embedded SVG tactical board.
    
    Args:
        plan: The tactical plan to visualize
        width: Width of the SVG in pixels
        height: Height of the SVG in pixels
    
    Returns:
        Complete HTML string with embedded SVG
    """
    svg_content = generate_svg_board(plan, width, height)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{plan.name} - Tactical Board</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: {width + 40}px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .svg-container {{
            text-align: center;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="svg-container">
            {svg_content}
        </div>
    </div>
</body>
</html>"""
    
    return html

