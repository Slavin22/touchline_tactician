"""Validation tools for tactical plans."""
from typing import List, Optional

from agno.tools import Toolkit
from agno.utils.log import log_debug, logger

from models.tactical_plan import TacticalPlan


class TacticalValidatorTools(Toolkit):
    """Tools for validating tactical plans."""
    
    def __init__(self, **kwargs):
        """Initialize tactical validator tools."""
        super().__init__(
            name="tactical_validator",
            tools=[
                self.validate_formation,
                self.validate_player_positions,
                self.validate_zones,
                self.check_tactical_consistency,
            ],
            **kwargs,
        )
    
    def validate_formation(self, plan: TacticalPlan) -> dict:
        """
        Validate that the formation is correct.
        
        Args:
            plan: The tactical plan to validate
        
        Returns:
            Validation result with status and messages
        """
        try:
            issues = []
            
            # Check formation format
            if not plan.formation or '-' not in plan.formation:
                issues.append("Formation must be in format like '4-3-3'")
            
            # Check player count matches formation
            if not plan.validate_formation():
                issues.append(
                    f"Number of players ({len(plan.players)}) doesn't match "
                    f"expected for formation {plan.formation}"
                )
            
            # Check for goalkeeper
            has_gk = any(p.position.upper() in ['GK', 'GOALKEEPER'] for p in plan.players)
            if not has_gk:
                issues.append("Team must have a goalkeeper (GK)")
            
            return {
                "valid": len(issues) == 0,
                "issues": issues,
                "message": "Formation is valid" if len(issues) == 0 else f"Found {len(issues)} issues"
            }
        
        except Exception as e:
            logger.error(f"Error validating formation: {e}")
            return {
                "valid": False,
                "issues": [str(e)],
                "message": f"Validation error: {e}"
            }
    
    def validate_player_positions(self, plan: TacticalPlan) -> dict:
        """
        Validate player positions are valid.
        
        Args:
            plan: The tactical plan to validate
        
        Returns:
            Validation result
        """
        try:
            issues = []
            
            valid_positions = [
                'GK', 'CB', 'LB', 'RB', 'LWB', 'RWB',
                'CDM', 'CM', 'CAM', 'LM', 'RM',
                'LW', 'RW', 'ST', 'CF'
            ]
            
            for player in plan.players:
                if player.position.upper() not in valid_positions:
                    issues.append(
                        f"Player {player.number} has invalid position: {player.position}"
                    )
            
            # Check for duplicate player numbers
            numbers = [p.number for p in plan.players]
            duplicates = [n for n in numbers if numbers.count(n) > 1]
            if duplicates:
                issues.append(f"Duplicate player numbers: {duplicates}")
            
            return {
                "valid": len(issues) == 0,
                "issues": issues,
                "message": "Player positions are valid" if len(issues) == 0 else f"Found {len(issues)} issues"
            }
        
        except Exception as e:
            logger.error(f"Error validating positions: {e}")
            return {
                "valid": False,
                "issues": [str(e)],
                "message": f"Validation error: {e}"
            }
    
    def validate_zones(self, plan: TacticalPlan) -> dict:
        """
        Validate that zones are properly defined and don't overlap incorrectly.
        
        Args:
            plan: The tactical plan to validate
        
        Returns:
            Validation result
        """
        try:
            issues = []
            
            # Check all players have zones
            for player in plan.players:
                if not player.zone:
                    issues.append(f"Player {player.number} is missing a zone")
            
            # Check zones are within field bounds (0-100)
            for player in plan.players:
                zone = player.zone
                if (zone.x_min < 0 or zone.x_max > 100 or
                    zone.y_min < 0 or zone.y_max > 100):
                    issues.append(f"Player {player.number} zone is out of bounds")
            
            return {
                "valid": len(issues) == 0,
                "issues": issues,
                "message": "Zones are valid" if len(issues) == 0 else f"Found {len(issues)} issues"
            }
        
        except Exception as e:
            logger.error(f"Error validating zones: {e}")
            return {
                "valid": False,
                "issues": [str(e)],
                "message": f"Validation error: {e}"
            }
    
    def check_tactical_consistency(self, plan: TacticalPlan) -> dict:
        """
        Check overall tactical consistency.
        
        Args:
            plan: The tactical plan to validate
        
        Returns:
            Validation result
        """
        try:
            issues = []
            
            # Check all players have phase instructions
            for player in plan.players:
                if not player.phases:
                    issues.append(f"Player {player.number} missing phase instructions")
                else:
                    required_phases = ['attack', 'defense', 'transition']
                    for phase in required_phases:
                        if phase not in player.phases:
                            issues.append(f"Player {player.number} missing {phase} phase instructions")
            
            # Check pressing triggers are defined
            if not plan.pressing_triggers:
                issues.append("No pressing triggers defined")
            
            return {
                "valid": len(issues) == 0,
                "issues": issues,
                "message": "Tactical plan is consistent" if len(issues) == 0 else f"Found {len(issues)} issues"
            }
        
        except Exception as e:
            logger.error(f"Error checking consistency: {e}")
            return {
                "valid": False,
                "issues": [str(e)],
                "message": f"Validation error: {e}"
            }

