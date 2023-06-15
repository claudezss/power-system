import enum
from typing import Optional, Tuple

from pydantic import BaseModel, Field


class AssetType(enum.Enum):
    """
    AssetType is an enumeration of the different types of assets that can be
    represented in a network model.
    """

    Node = "Node"
    Line = "Line"
    Load = "Load"
    Transformer = "Transformer"
    Switch = "Switch"
    Generator = "Generator"
    Battery = "Battery"
    PV = "PV"
    Solar = "Solar"
    Wind = "Wind"


class Model(BaseModel):
    id: str = Field(..., alias="id")
    name: str = Field(..., alias="name")
    coordinates: Optional[Tuple[float, float]] = Field(..., alias="coordinates", default=None)
    asset_type: AssetType = Field(..., alias="asset_type")
