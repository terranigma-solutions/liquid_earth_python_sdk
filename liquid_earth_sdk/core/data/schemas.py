from dataclasses import dataclass
from typing import Optional


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
    
    
@dataclass
class DeleteSpacePostData:
    spaceId: str


@dataclass
class ChangeSpaceRolePostData:
    spaceId: str
    ownerId: str
    targetEmail: str
    permissions: int


@dataclass
class ImportDataToSpacePostData:
    spaceId: str
    ownerId: str
    path_in: str
    type_of_import: str
    path_out: str | None = None
    transformation: dict | None = None
    attr_name: str | None = None
    missing_value: float | None = None
    band: int | None = None
    collar_reader: dict | None = None
    survey_reader: dict | None = None
    attrs_reader: dict | None = None
    is_lith_attr: bool | None = None
    number_nodes: int | None = None
    vertex_reader: dict | None = None
    edges_reader: dict | None = None
    cells_attrs_reader: dict | None = None
    vertex_attrs_reader: dict | None = None
    coord_reader: dict | None = None
    interpolation_resolution: list | None = None
    path_in_msh: str | None = None
    path_in_mod_or_den: str | None = None


@dataclass
class GetSpaceUpdatesPostData:
    spaceId: str