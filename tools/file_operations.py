"""File operations for tactical plans."""
import json
from pathlib import Path
from typing import Optional
from uuid import UUID

from agno.tools import Toolkit
from agno.utils.log import log_debug, logger

from models.tactical_plan import TacticalPlan


class TacticalPlanFileTools(Toolkit):
    """Tools for reading and writing tactical plan files."""
    
    def __init__(
        self,
        plans_directory: str = "storage/plans",
        **kwargs,
    ):
        """
        Initialize tactical plan file tools.
        
        Args:
            plans_directory: Directory where plan files are stored
        """
        self.plans_directory = Path(plans_directory)
        self.plans_directory.mkdir(parents=True, exist_ok=True)
        
        super().__init__(
            name="tactical_plan_files",
            tools=[
                self.save_plan,
                self.load_plan,
                self.list_plans,
                self.delete_plan,
            ],
            **kwargs,
        )
    
    def save_plan(self, plan: TacticalPlan, filename: Optional[str] = None) -> str:
        """
        Save a tactical plan to a JSON file.
        
        Args:
            plan: The tactical plan to save
            filename: Optional filename. If not provided, uses plan_id.json
        
        Returns:
            Path to the saved file
        """
        try:
            if filename is None:
                filename = f"{plan.plan_id}.json"
            
            if not filename.endswith('.json'):
                filename += '.json'
            
            filepath = self.plans_directory / filename
            
            # Update modified time before saving
            plan.update_modified_time()
            
            # Convert to dict and handle UUID serialization
            plan_dict = plan.model_dump(mode='json')
            plan_dict['plan_id'] = str(plan_dict['plan_id'])
            
            with open(filepath, 'w') as f:
                json.dump(plan_dict, f, indent=2)
            
            log_debug(f"Saved tactical plan to {filepath}")
            return str(filepath)
        
        except Exception as e:
            logger.error(f"Error saving plan: {e}")
            raise
    
    def load_plan(self, filename: str) -> TacticalPlan:
        """
        Load a tactical plan from a JSON file.
        
        Args:
            filename: Name of the plan file (with or without .json extension)
        
        Returns:
            The loaded tactical plan
        """
        try:
            if not filename.endswith('.json'):
                filename += '.json'
            
            filepath = self.plans_directory / filename
            
            if not filepath.exists():
                raise FileNotFoundError(f"Plan file not found: {filepath}")
            
            with open(filepath, 'r') as f:
                plan_dict = json.load(f)
            
            # Convert plan_id string back to UUID
            if 'plan_id' in plan_dict:
                plan_dict['plan_id'] = UUID(plan_dict['plan_id'])
            
            plan = TacticalPlan(**plan_dict)
            log_debug(f"Loaded tactical plan from {filepath}")
            return plan
        
        except Exception as e:
            logger.error(f"Error loading plan: {e}")
            raise
    
    def list_plans(self) -> list[str]:
        """
        List all available tactical plan files.
        
        Returns:
            List of plan filenames
        """
        try:
            plan_files = list(self.plans_directory.glob("*.json"))
            return [f.stem for f in plan_files]
        
        except Exception as e:
            logger.error(f"Error listing plans: {e}")
            return []
    
    def delete_plan(self, filename: str) -> str:
        """
        Delete a tactical plan file.
        
        Args:
            filename: Name of the plan file to delete
        
        Returns:
            Confirmation message
        """
        try:
            if not filename.endswith('.json'):
                filename += '.json'
            
            filepath = self.plans_directory / filename
            
            if not filepath.exists():
                raise FileNotFoundError(f"Plan file not found: {filepath}")
            
            filepath.unlink()
            log_debug(f"Deleted tactical plan: {filepath}")
            return f"Deleted plan: {filename}"
        
        except Exception as e:
            logger.error(f"Error deleting plan: {e}")
            raise

