from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class ActionSchema(BaseModel):
    id: str
    type: str
    parameters: Dict[str, Any]

class StepSchema(BaseModel):
    id: str
    name: str
    action: ActionSchema
    next_step: Optional[str] = None
    on_failure: Optional[str] = None

class PlaybookSchema(BaseModel):
    id: str
    version: str = "1.0.0"
    name: str
    description: Optional[str]
    trigger_condition: Dict[str, Any]
    steps: List[StepSchema]
