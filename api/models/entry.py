# # from pydantic import BaseModel, Field, field_validator
# # from typing import Optional
# # from datetime import datetime
# # from uuid import uuid4
# # import uuid
# # import bleach

# # SCHEMA_VERSION = "1.0"


# # class Entry(BaseModel):
# #     # TODO: Add field validation rules
# #     # TODO: Add custom validators
# #     # TODO: Add schema versioning
# #     # TODO: Add data sanitization methods

# #     id: str = Field(
# #         default_factory=lambda: str(uuid4()),
# #         description="Unique identifier for the entry (UUID)."
# #     )
# #     work: str = Field(
# #         ...,
# #         max_length=256,
# #         description="What did you work on today?"
# #     )
# #     struggle: str = Field(
# #         ...,
# #         max_length=256,
# #         description="What’s one thing you struggled with today?"
# #     )
# #     intention: str = Field(
# #         ...,
# #         max_length=256,
# #         description="What will you study/work on tomorrow?"
# #     )
# #     created_at: Optional[datetime] = Field(
# #         default_factory=datetime.utcnow,
# #         description="Timestamp when the entry was created."
# #     )
# #     updated_at: Optional[datetime] = Field(
# #         default_factory=datetime.utcnow,
# #         description="Timestamp when the entry was last updated."
# #     )
# #     schema_version: str = Field(
# #         default=SCHEMA_VERSION,
# #         description="Version of the schema used for this entry."
# #     )
# #     # Optional: add a partition key if your Cosmos DB collection requires it
# #     # partition_key: str = Field(..., description="Partition key for the entry.")

# #     @field_validator('work', 'struggle', 'intention', mode='before')
# #     @classmethod
# #     def sanitize_text(cls, v):
# #         if not isinstance(v, str):
# #             raise ValueError("Must be a string")
# #         return bleach.clean(v, strip=True).strip()

# #     @field_validator('id')
# #     @classmethod
# #     def validate_uuid(cls, v):
# #         try:
# #             uuid.UUID(str(v))
# #         except ValueError:
# #             raise ValueError("id must be a valid UUID string")
# #         return v

# #     class Config:
# #         # Example: allow_population_by_field_name = True
# #         pass


# # from pydantic import BaseModel, Field, field_validator
# # from typing import Optional
# # from datetime import datetime
# # from uuid import UUID, uuid4
# # import bleach

# # SCHEMA_VERSION = "1.0"


# # class Entry(BaseModel):
# #     id: UUID = Field(
# #         default_factory=uuid4,
# #         description="Unique identifier for the entry (UUID)."
# #     )
# #     work: str = Field(..., max_length=256)
# #     struggle: str = Field(..., max_length=256)
# #     intention: str = Field(..., max_length=256)
# #     created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
# #     updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
# #     schema_version: str = Field(default=SCHEMA_VERSION)

# #     @field_validator('work', 'struggle', 'intention', mode='before')
# #     @classmethod
# #     def sanitize_text(cls, v):
# #         if not isinstance(v, str):
# #             raise ValueError("Must be a string")
# #         return bleach.clean(v, strip=True).strip()

# #     model_config = {
# #         "from_attributes": True
# #     }  # So SQLAlchemy or Mongoengine objects work


# from pydantic import BaseModel, Field, field_validator
# from datetime import datetime, timezone
# from uuid import UUID, uuid4
# from typing import ClassVar
# import bleach


# class Entry(BaseModel):
#     """
#     Journal Entry Model matching PostgreSQL schema:
#     - id: Auto-generated UUID (string format)
#     - work: Required, max 256 chars
#     - struggle: Required, max 256 chars
#     - intention: Required, max 256 chars
#     - created_at: Auto-generated timezone-aware UTC
#     - updated_at: Auto-updated timezone-aware UTC
#     """

#     MAX_LENGTH: ClassVar[int] = 256

#     id: str = Field(
#         default_factory=lambda: str(uuid4()),
#         description="Auto-generated UUID in string format"
#     )
#     work: str = Field(
#         ...,
#         max_length=MAX_LENGTH,
#         description="What you worked on (required, max 256 chars)"
#     )
#     struggle: str = Field(
#         ...,
#         max_length=MAX_LENGTH,
#         description="What you struggled with (required, max 256 chars)"
#     )
#     intention: str = Field(
#         ...,
#         max_length=MAX_LENGTH,
#         description="Your intention for tomorrow (required, max 256 chars)"
#     )
#     created_at: datetime = Field(
#         default_factory=lambda: datetime.now(timezone.utc),
#         description="Auto-generated timezone-aware UTC timestamp"
#     )
#     updated_at: datetime = Field(
#         default_factory=lambda: datetime.now(timezone.utc),
#         description="Auto-updated timezone-aware UTC timestamp"
#     )

#     @field_validator('work', 'struggle', 'intention')
#     @classmethod
#     def validate_text_fields(cls, value: str) -> str:
#         """Validate and sanitize text fields"""
#         if not isinstance(value, str):
#             raise ValueError("Must be a string")

#         sanitized = bleach.clean(value.strip(), strip=True)

#         if len(sanitized) > cls.MAX_LENGTH:
#             raise ValueError(
#                 f"Field must be {cls.MAX_LENGTH} characters or fewer")

#         if not sanitized:
#             raise ValueError("Field cannot be empty")

#         return sanitized

#     class Config:
#         json_schema_extra = {
#             "example": {
#                 "work": "Implemented user authentication",
#                 "struggle": "JWT token expiration handling",
#                 "intention": "Work on refresh token implementation"
#             }
#         }

from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timezone
from uuid import UUID, uuid4
from typing import ClassVar
import bleach


class Entry(BaseModel):
    """
    Journal Entry Model matching PostgreSQL schema:
    - id: Auto-generated UUID
    - work: Required, max 256 chars
    - struggle: Required, max 256 chars
    - intention: Required, max 256 chars
    - created_at: Auto-generated timezone-aware UTC
    - updated_at: Auto-updated timezone-aware UTC
    """

    MAX_LENGTH: ClassVar[int] = 256

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique identifier for the entry (UUID)."
    )

    work: str = Field(
        ...,
        max_length=MAX_LENGTH,
        description="What you worked on (required, max 256 chars)"
    )
    struggle: str = Field(
        ...,
        max_length=MAX_LENGTH,
        description="What you struggled with (required, max 256 chars)"
    )
    intention: str = Field(
        ...,
        max_length=MAX_LENGTH,
        description="Your intention for tomorrow (required, max 256 chars)"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Auto-generated timezone-aware UTC timestamp"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Auto-updated timezone-aware UTC timestamp"
    )

    @field_validator('work', 'struggle', 'intention')
    @classmethod
    def validate_text_fields(cls, value: str) -> str:
        """Validate and sanitize text fields"""
        if not isinstance(value, str):
            raise ValueError("Must be a string")

        sanitized = bleach.clean(value.strip(), strip=True)

        if len(sanitized) > cls.MAX_LENGTH:
            raise ValueError(
                f"Field must be {cls.MAX_LENGTH} characters or fewer")

        if not sanitized:
            raise ValueError("Field cannot be empty")

        return sanitized

    class Config:
        json_schema_extra = {
            "example": {
                "work": "Implemented user authentication",
                "struggle": "JWT token expiration handling",
                "intention": "Work on refresh token implementation"
            }
        }
