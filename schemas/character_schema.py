from pydantic import BaseModel, field_validator
from typing import Optional
import re

from models.character import Vocation


class CharacterCreate(BaseModel):
    # Input schema — validates data coming from the creation form.
    name: str
    server_id: int
    vocation: Optional[str] = None  # Empty string from form becomes None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        value = value.strip()
        if not re.match(r"^[a-zA-Z ]{2,30}$", value):
            raise ValueError(
                "Name must be 2-30 characters long and contain only letters and spaces."
            )
        return value

    @field_validator("vocation")
    @classmethod
    def validate_vocation(cls, value):
        # Empty string from the Rookie option is converted to None.
        if not value:
            return None
        # Check if the value matches a valid Vocation enum member.
        valid_vocations = [v.value for v in Vocation]
        if value not in valid_vocations:
            raise ValueError(f"Invalid vocation. Must be one of: {valid_vocations}")
        return value


class CharacterEdit(BaseModel):
    # Same fields as creation — server is editable due to server transfers.
    name: str
    server_id: int
    vocation: Optional[str] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        value = value.strip()
        if not re.match(r"^[a-zA-Z ]{2,30}$", value):
            raise ValueError(
                "Name must be 2-30 characters long and contain only letters and spaces."
            )
        return value

    @field_validator("vocation")
    @classmethod
    def validate_vocation(cls, value):
        if not value:
            return None
        valid_vocations = [v.value for v in Vocation]
        if value not in valid_vocations:
            raise ValueError(f"Invalid vocation. Must be one of: {valid_vocations}")
        return value


class CharacterResponse(BaseModel):
    # Output schema — defines what is exposed to the template.
    id: int
    name: str
    vocation: Optional[Vocation] = None
    server_id: int

    model_config = {"from_attributes": True}