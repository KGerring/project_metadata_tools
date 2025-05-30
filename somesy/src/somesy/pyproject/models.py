"""Pyproject models."""

from enum import Enum
from logging import getLogger
from pathlib import Path
from typing import Dict, List, Optional, Set, Union

from packaging.version import parse as parse_version
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    TypeAdapter,
    field_validator,
    model_validator,
)
from typing_extensions import Annotated

from somesy.core.models import LicenseEnum
from somesy.core.types import HttpUrlStr

EMailAddress = TypeAdapter(EmailStr)
logger = getLogger("somesy")


class STPerson(BaseModel):
    """Person model for setuptools."""

    name: Annotated[str, Field(min_length=1)]
    email: Annotated[Optional[str], Field(min_length=1)] = None

    def __str__(self):
        """Return string representation of STPerson."""
        if self.email:
            return f"{self.name} <{self.email}>"
        else:
            return self.name


class License(BaseModel):
    """License model for setuptools."""

    model_config = dict(validate_assignment=True)

    file: Optional[Path] = None
    text: Optional[LicenseEnum] = None

    @model_validator(mode="before")
    @classmethod
    def validate_xor(cls, values):
        """Validate that only one of file or text is set."""
        # check if this has just str or list of str
        if isinstance(values, str):
            if values in LicenseEnum.__members__:
                return {"text": values}
            else:
                raise ValueError("Invalid license.")
        if isinstance(values, list):
            # check if all elements are valid string for LicenseEnum
            for v in values:
                if not isinstance(v, str):
                    raise ValueError("All elements must be strings.")
                if v not in LicenseEnum.__members__:
                    raise ValueError("Invalid license.")
            return values
        if sum([bool(v) for v in values.values()]) != 1:
            raise ValueError("Either file or text must be set.")
        return values


class PoetryConfig(BaseModel):
    """Poetry configuration model."""

    model_config = dict(use_enum_values=True)

    name: Annotated[
        str,
        Field(pattern=r"^[A-Za-z0-9]+([_-][A-Za-z0-9]+)*$", description="Package name"),
    ]
    version: Annotated[
        str,
        Field(
            pattern=r"^\d+(\.\d+)*((a|b|rc)\d+)?(post\d+)?(dev\d+)?$",
            description="Package version",
        ),
    ]
    description: Annotated[str, Field(description="Package description")]
    license: Annotated[
        Optional[Union[LicenseEnum, List[LicenseEnum], License]],
        Field(description="An SPDX license identifier."),
    ]

    # v1 has str, v2 has STPerson
    authors: Annotated[List[Union[str, STPerson]], Field(description="Package authors")]
    maintainers: Annotated[
        Optional[List[Union[str, STPerson]]], Field(description="Package maintainers")
    ] = None

    readme: Annotated[
        Optional[Union[Path, List[Path]]], Field(description="Package readme file(s)")
    ] = None
    homepage: Annotated[Optional[HttpUrlStr], Field(description="Package homepage")] = (
        None
    )
    repository: Annotated[
        Optional[HttpUrlStr], Field(description="Package repository")
    ] = None
    documentation: Annotated[
        Optional[HttpUrlStr], Field(description="Package documentation page")
    ] = None
    keywords: Annotated[
        Optional[Set[str]], Field(description="Keywords that describe the package")
    ] = None
    classifiers: Annotated[
        Optional[List[str]], Field(description="pypi classifiers")
    ] = None
    urls: Annotated[
        Optional[Dict[str, HttpUrlStr]], Field(description="Package URLs")
    ] = None

    @field_validator("version")
    @classmethod
    def validate_version(cls, v):
        """Validate version using PEP 440."""
        try:
            _ = parse_version(v)
        except ValueError as err:
            raise ValueError("Invalid version") from err
        return v

    @field_validator("authors", "maintainers")
    @classmethod
    def validate_email_format(cls, v):
        """Validate person format, omit person that is not in correct format, don't raise an error."""
        if v is None:
            return []
        validated = []
        seen = set()
        for author in v:
            if isinstance(author, STPerson) and author.email:
                if not EMailAddress.validate_python(author.email):
                    logger.warning(
                        f"Invalid email format for author/maintainer {author}."
                    )
                else:
                    author_str = str(author)
                    if author_str not in seen:
                        seen.add(author_str)
                        validated.append(author)
                    else:
                        logger.warning(f"Same person {author} is added multiple times.")
            elif "@" in author and EMailAddress.validate_python(
                author.split(" ")[-1][1:-1]
            ):
                validated.append(author)
            else:
                author_str = str(author)
                if author_str not in seen:
                    seen.add(author_str)
                    validated.append(author)
                else:
                    logger.warning(f"Same person {author} is added multiple times.")

        return validated

    @field_validator("readme")
    @classmethod
    def validate_readme(cls, v):
        """Validate readme file(s) by checking whether files exist."""
        if isinstance(v, list):
            if any(not e.is_file() for e in v):
                logger.warning("Some readme file(s) do not exist")
        else:
            if not v.is_file():
                logger.warning("Readme file does not exist")


class ContentTypeEnum(Enum):
    """Content type enum for setuptools field file."""

    plain = "text/plain"
    rst = "text/x-rst"
    markdown = "text/markdown"


class File(BaseModel):
    """File model for setuptools."""

    file: Path
    content_type: Optional[ContentTypeEnum] = Field(alias="content-type")


class URLs(BaseModel):
    """URLs model for setuptools."""

    homepage: Optional[HttpUrlStr] = None
    repository: Optional[HttpUrlStr] = None
    documentation: Optional[HttpUrlStr] = None
    changelog: Optional[HttpUrlStr] = None


class SetuptoolsConfig(BaseModel):
    """Setuptools input model. Required fields are name, version, description, and requires_python."""

    model_config = dict(use_enum_values=True)

    name: Annotated[str, Field(pattern=r"^[A-Za-z0-9]+([_-][A-Za-z0-9]+)*$")]
    version: Annotated[
        str, Field(pattern=r"^\d+(\.\d+)*((a|b|rc)\d+)?(post\d+)?(dev\d+)?$")
    ]
    description: str
    readme: Optional[Union[Path, List[Path], File]] = None
    license: Optional[License] = Field(None, description="An SPDX license identifier.")
    authors: Optional[List[STPerson]] = None
    maintainers: Optional[List[STPerson]] = None
    keywords: Optional[Set[str]] = None
    classifiers: Optional[List[str]] = None
    urls: Optional[URLs] = None

    @field_validator("version")
    @classmethod
    def validate_version(cls, v):
        """Validate version using PEP 440."""
        try:
            _ = parse_version(v)
        except ValueError as err:
            raise ValueError("Invalid version") from err
        return v

    @field_validator("readme")
    @classmethod
    def validate_readme(cls, v):
        """Validate readme file(s) by checking whether files exist."""
        if isinstance(v, list):
            if any(not e.is_file() for e in v):
                raise ValueError("Some file(s) do not exist")
        elif type(v) is File:
            if not Path(v.file).is_file():
                raise ValueError("File does not exist")
        else:
            if not v.is_file():
                raise ValueError("File does not exist")

    @field_validator("authors", "maintainers")
    @classmethod
    def validate_email_format(cls, v):
        """Validate email format."""
        for person in v:
            if person.email:
                if not EMailAddress.validate_python(person.email):
                    raise ValueError("Invalid email format")
        return v
