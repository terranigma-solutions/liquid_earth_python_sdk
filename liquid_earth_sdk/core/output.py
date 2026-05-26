import dataclasses
from typing import Optional
from pydantic import BaseModel


class AvailableProject(BaseModel):
    CreationDate: Optional[str] = None
    DisplayedOwner: str
    Name: Optional[str] = None
    OwnerId: str
    SpaceId: str


@dataclasses.dataclass
class ServerResponse:
    deep_link: str = None
    available_projects: Optional[list[AvailableProject]] = None
    selected_project: Optional[AvailableProject] = None
    
    
