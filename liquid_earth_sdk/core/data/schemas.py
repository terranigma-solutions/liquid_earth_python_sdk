from dataclasses import dataclass
from typing import Optional, List


@dataclass
class AddDataPostData:
    spaceId: str
    ownerId: str
    dataType: str
    fileName: str
    texture_ext: Optional[str] = None


@dataclass
class AddNewSpacePostData:
    spaceName: str
    # Optional space extent as [minX, maxX, minY, maxY, minZ, maxZ].
    # When None the backend uses its default unit cube extent.
    extent: Optional[List[float]] = None
    
    
@dataclass
class DeleteSpacePostData:
    spaceId: str