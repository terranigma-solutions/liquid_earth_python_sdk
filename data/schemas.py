from dataclasses import dataclass


@dataclass
class PostData:
    spaceId: str
    ownerId: str
    dataType: str
    fileName: str