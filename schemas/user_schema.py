from pydantic import BaseModel, field_validator
import re


class UserCreate(BaseModel):
    # Input schema — validates data coming from the form.
    # name must be 3-20 characters, letters, numbers and underscores only.
    name: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        value = value.strip()

        if not re.match(r"^[a-zA-Z0-9_]{3,20}$", value):
            raise ValueError(
                "Name must be 3-20 characters long and contain only "
                "letters, numbers and underscores."
            )
        return value


class UserResponse(BaseModel):
    # Output schema — defines what is exposed to the template.
    id: int
    name: str

    # This tells Pydantic to read data from SQLAlchemy model attributes
    # instead of expecting a plain dictionary.
    model_config = {"from_attributes": True}