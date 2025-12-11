"""Validation tools for tactical plans."""
import json
import re
from pathlib import Path
from typing import List, Optional, Union
from uuid import UUID

from agno.tools import Toolkit
from agno.utils.log import log_debug, logger

from models.tactical_plan import TacticalPlan


class TacticalValidatorTools(Toolkit):
    """Tools for validating tactical plans."""
    
    def __init__(self, plans_directory: str = "storage/plans", **kwargs):
        """
        Initialize tactical validator tools.
        
        Args:
            plans_directory: Directory where plan files are stored (used for loading plans by ID)
        """
        self.plans_directory = Path(plans_directory)
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
    
    def _parse_plan(self, plan: Union[str, dict, TacticalPlan]) -> TacticalPlan:
        """
        Parse plan input into a TacticalPlan object.
        
        Args:
            plan: Can be a TacticalPlan object, a dict, a JSON string, or a plan_id (UUID string)
                  If a plan_id is provided, the plan will be loaded from the file system
            
        Returns:
            TacticalPlan object
        """
        if isinstance(plan, TacticalPlan):
            return plan
        elif isinstance(plan, dict):
            # Handle plan_id conversion if present
            if 'plan_id' in plan and isinstance(plan['plan_id'], str):
                try:
                    plan['plan_id'] = UUID(plan['plan_id'])
                except (ValueError, TypeError):
                    # Not a valid UUID, let it be auto-generated
                    del plan['plan_id']
            return TacticalPlan(**plan)
        elif isinstance(plan, str):
            # Try to parse as JSON string first
            try:
                plan_dict = json.loads(plan)
                if 'plan_id' in plan_dict and isinstance(plan_dict['plan_id'], str):
                    try:
                        plan_dict['plan_id'] = UUID(plan_dict['plan_id'])
                    except (ValueError, TypeError):
                        # Not a valid UUID, let it be auto-generated
                        del plan_dict['plan_id']
                return TacticalPlan(**plan_dict)
            except (json.JSONDecodeError, TypeError):
                # If it's not JSON, check if it's a valid UUID (plan_id)
                # or a string representation of a TacticalPlan object (e.g., "plan_id=UUID('...') name='...'")
                plan_uuid = None
                
                # First, try to extract UUID from string representation of TacticalPlan
                # Pattern: plan_id=UUID('...') or plan_id=UUID("...")
                uuid_match = re.search(r"plan_id=UUID\(['\"]([^'\"]+)['\"]\)", plan)
                if uuid_match:
                    try:
                        plan_uuid = UUID(uuid_match.group(1))
                    except (ValueError, TypeError):
                        pass
                
                # If no UUID found in string representation, try parsing the whole string as UUID
                if plan_uuid is None:
                    try:
                        plan_uuid = UUID(plan.strip())
                    except (ValueError, TypeError):
                        # Not a valid UUID - might be a filename instead
                        plan_uuid = None
                
                # Try to load from file using UUID if we have one
                if plan_uuid is not None:
                    plan_file = self.plans_directory / f"{plan_uuid}.json"
                    if plan_file.exists():
                        try:
                            with open(plan_file, 'r') as f:
                                plan_dict = json.load(f)
                            # Convert plan_id string back to UUID
                            if 'plan_id' in plan_dict and isinstance(plan_dict['plan_id'], str):
                                plan_dict['plan_id'] = UUID(plan_dict['plan_id'])
                            return TacticalPlan(**plan_dict)
                        except (json.JSONDecodeError, KeyError, ValueError) as e:
                            raise ValueError(
                                f"Error loading plan file for plan_id {plan_uuid}: {e}. "
                                f"The file may be corrupted or incomplete."
                            )
                    else:
                        raise ValueError(
                            f"Plan file not found for plan_id: {plan_uuid}. "
                            f"The plan may not have been saved yet, or the plan_id is incorrect."
                        )
                
                # If not a UUID, try treating it as a filename
                plan_file = self.plans_directory / plan.strip()
                if not plan_file.suffix:
                    plan_file = plan_file.with_suffix('.json')
                elif plan_file.suffix != '.json':
                    plan_file = plan_file.with_suffix('.json')
                
                if plan_file.exists():
                    try:
                        with open(plan_file, 'r') as f:
                            plan_dict = json.load(f)
                        # Convert plan_id string back to UUID
                        if 'plan_id' in plan_dict and isinstance(plan_dict['plan_id'], str):
                            plan_dict['plan_id'] = UUID(plan_dict['plan_id'])
                        return TacticalPlan(**plan_dict)
                    except (json.JSONDecodeError, KeyError, ValueError) as e:
                        raise ValueError(
                            f"Error loading plan file {plan_file.name}: {e}. "
                            f"The file may be corrupted or incomplete."
                        )
                else:
                    # Neither UUID nor filename worked
                    raise ValueError(
                        f"Invalid plan input: expected TacticalPlan, dict, JSON string, plan_id (UUID), or filename. "
                        f"Tried to load as UUID and filename, but neither worked. Input: {plan[:100]}"
                    )
        else:
            raise TypeError(
                f"Invalid plan type: expected TacticalPlan, dict, or JSON string, got {type(plan)}"
            )
    
    def validate_formation(self, plan: Union[str, dict, TacticalPlan]) -> dict:
        """
        Validate that the formation is correct.
        
        Args:
            plan: The tactical plan to validate (can be a TacticalPlan object, dict, JSON string, or plan_id UUID string)
        
        Returns:
            Validation result with status and messages
        """
        try:
            plan_obj = self._parse_plan(plan)
            issues = []
            
            # Check formation format
            if not plan_obj.formation or '-' not in plan_obj.formation:
                issues.append("Formation must be in format like '4-3-3'")
            
            # Check player count matches formation
            if not plan_obj.validate_formation():
                issues.append(
                    f"Number of players ({len(plan_obj.players)}) doesn't match "
                    f"expected for formation {plan_obj.formation}"
                )
            
            # Check for goalkeeper
            has_gk = any(p.position.upper() in ['GK', 'GOALKEEPER'] for p in plan_obj.players)
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
    
    def validate_player_positions(self, plan: Union[str, dict, TacticalPlan]) -> dict:
        """
        Validate player positions are valid.
        
        Args:
            plan: The tactical plan to validate (can be a TacticalPlan object, dict, JSON string, or plan_id UUID string)
        
        Returns:
            Validation result
        """
        try:
            plan_obj = self._parse_plan(plan)
            issues = []
            
            valid_positions = [
                'GK', 'CB', 'LB', 'RB', 'LWB', 'RWB',
                'CDM', 'CM', 'CAM', 'LM', 'RM',
                'LW', 'RW', 'ST', 'CF'
            ]
            
            for player in plan_obj.players:
                if player.position.upper() not in valid_positions:
                    issues.append(
                        f"Player {player.number} has invalid position: {player.position}"
                    )
            
            # Check for duplicate player numbers
            numbers = [p.number for p in plan_obj.players]
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
    
    def validate_zones(self, plan: Union[str, dict, TacticalPlan]) -> dict:
        """
        Validate that zones are properly defined and don't overlap incorrectly.
        
        Args:
            plan: The tactical plan to validate (can be a TacticalPlan object, dict, JSON string, or plan_id UUID string)
        
        Returns:
            Validation result
        """
        try:
            plan_obj = self._parse_plan(plan)
            issues = []
            
            # Check all players have zones
            for player in plan_obj.players:
                if not player.zone:
                    issues.append(f"Player {player.number} is missing a zone")
            
            # Check zones are within field bounds (0-100)
            for player in plan_obj.players:
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
    
    def check_tactical_consistency(self, plan: Union[str, dict, TacticalPlan]) -> dict:
        """
        Check overall tactical consistency.
        
        Args:
            plan: The tactical plan to validate (can be a TacticalPlan object, dict, JSON string, or plan_id UUID string)
        
        Returns:
            Validation result
        """
        try:
            plan_obj = self._parse_plan(plan)
            issues = []
            
            # Check all players have phase instructions
            for player in plan_obj.players:
                if not player.phases:
                    issues.append(f"Player {player.number} missing phase instructions")
                else:
                    required_phases = ['attack', 'defense', 'transition']
                    for phase in required_phases:
                        if phase not in player.phases:
                            issues.append(f"Player {player.number} missing {phase} phase instructions")
            
            # Check pressing triggers are defined
            if not plan_obj.pressing_triggers:
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

