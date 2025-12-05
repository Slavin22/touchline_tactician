"""Tactical plan data models using Pydantic."""
from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


class Zone(BaseModel):
    """Represents a zone on the tactical board."""
    x_min: float = Field(ge=0, le=100, description="Minimum x coordinate (0-100)")
    x_max: float = Field(ge=0, le=100, description="Maximum x coordinate (0-100)")
    y_min: float = Field(ge=0, le=100, description="Minimum y coordinate (0-100)")
    y_max: float = Field(ge=0, le=100, description="Maximum y coordinate (0-100)")
    
    @field_validator('x_max')
    @classmethod
    def validate_x_range(cls, v, info):
        if 'x_min' in info.data and v <= info.data['x_min']:
            raise ValueError('x_max must be greater than x_min')
        return v
    
    @field_validator('y_max')
    @classmethod
    def validate_y_range(cls, v, info):
        if 'y_min' in info.data and v <= info.data['y_min']:
            raise ValueError('y_max must be greater than y_min')
        return v


class PlayerPhase(BaseModel):
    """Player responsibilities in a specific game phase."""
    position: str = Field(description="Position in this phase")
    responsibilities: List[str] = Field(default_factory=list, description="List of responsibilities")
    movement_patterns: List[str] = Field(default_factory=list, description="Movement patterns")
    key_actions: List[str] = Field(default_factory=list, description="Key actions to perform")


class Player(BaseModel):
    """Represents a player in the tactical plan."""
    number: int = Field(ge=1, le=99, description="Player jersey number")
    name: Optional[str] = Field(default=None, description="Player name")
    position: str = Field(description="Primary position (e.g., GK, CB, CM, LW, ST)")
    zone: Zone = Field(description="Player's zone on the field")
    responsibilities: Dict[str, str] = Field(default_factory=dict, description="General responsibilities")
    phases: Dict[str, PlayerPhase] = Field(
        default_factory=dict,
        description="Phase-specific instructions (attack, defense, transition)"
    )


class TacticalPlan(BaseModel):
    """Complete tactical plan structure."""
    plan_id: UUID = Field(default_factory=uuid4, description="Unique plan identifier")
    name: str = Field(description="Plan name")
    formation: str = Field(description="Formation (e.g., 4-3-3, 4-4-2)")
    players: List[Player] = Field(default_factory=list, description="List of players")
    zones: Dict[str, Zone] = Field(default_factory=dict, description="Team zones")
    pressing_triggers: List[str] = Field(default_factory=list, description="Pressing trigger conditions")
    transition_instructions: Dict[str, str] = Field(
        default_factory=dict,
        description="Transition instructions (attack_to_defense, defense_to_attack)"
    )
    metadata: Dict[str, str] = Field(
        default_factory=lambda: {
            "created_at": datetime.now().isoformat(),
            "modified_at": datetime.now().isoformat(),
        },
        description="Plan metadata"
    )
    
    def update_modified_time(self):
        """Update the modified_at timestamp."""
        self.metadata["modified_at"] = datetime.now().isoformat()
    
    def get_player_by_number(self, number: int) -> Optional[Player]:
        """Get a player by their jersey number."""
        for player in self.players:
            if player.number == number:
                return player
        return None
    
    def validate_formation(self) -> bool:
        """Validate that the formation matches the number of players."""
        # Basic validation - can be expanded
        standard_formations = {
            "4-3-3": 10,  # Outfield players
            "4-4-2": 10,
            "4-2-3-1": 10,
            "3-5-2": 10,
            "3-4-3": 10,
            "5-3-2": 10,
            "4-5-1": 10,
        }
        
        if self.formation in standard_formations:
            expected_players = standard_formations[self.formation] + 1  # +1 for goalkeeper
            return len(self.players) == expected_players
        
        return True  # Allow custom formations

