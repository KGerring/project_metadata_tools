"""Project documentation with Markdown (MkDocs) parser and saver."""

import logging
from pathlib import Path
from typing import List, Optional, Union

from rich.pretty import pretty_repr
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString

from somesy.core.models import Entity, Person, ProjectMetadata
from somesy.core.writer import FieldKeyMapping, IgnoreKey, ProjectMetadataWriter
from somesy.mkdocs.models import MkDocsConfig

logger = logging.getLogger("somesy")


class MkDocs(ProjectMetadataWriter):
    """Project documentation with Markdown (MkDocs) parser and saver."""

    def __init__(
        self,
        path: Path,
        create_if_not_exists: bool = False,
        pass_validation: Optional[bool] = False,
    ):
        """Project documentation with Markdown (MkDocs) parser.

        See [somesy.core.writer.ProjectMetadataWriter.__init__][].
        """
        self._yaml = YAML()
        self._yaml.preserve_quotes = True

        mappings: FieldKeyMapping = {
            "name": ["site_name"],
            "description": ["site_description"],
            "homepage": ["site_url"],
            "repository": ["repo_url"],
            "authors": ["site_author"],
            "documentation": IgnoreKey(),
            "version": IgnoreKey(),
            "maintainers": IgnoreKey(),
            "license": IgnoreKey(),
            "keywords": IgnoreKey(),
        }
        super().__init__(
            path,
            create_if_not_exists=create_if_not_exists,
            direct_mappings=mappings,
            pass_validation=pass_validation,
        )

    def _load(self):
        """Load the MkDocs file."""
        with open(self.path) as f:
            self._data = self._yaml.load(f)

    def _validate(self) -> None:
        """Validate the MkDocs file."""
        if self.pass_validation:
            return
        config = dict(self._get_property([]))
        logger.debug(
            f"Validating config using {MkDocsConfig.__name__}: {pretty_repr(config)}"
        )
        MkDocsConfig(**config)

    def save(self, path: Optional[Path] = None) -> None:
        """Save the MkDocs object to a file."""
        path = path or self.path

        # if description have new line characters, it should be saved as multiline string
        if self._data is not None and "site_description" in self._data:
            if "\n" in self._data["site_description"]:
                self._data["site_description"] = LiteralScalarString(
                    self._data["site_description"]
                )
            else:
                self._data["site_description"] = str(self.description)

        self._yaml.dump(self._data, path)

    @property
    def authors(self):
        """Return the only author from the source file as list."""
        authors = self._get_property(self._get_key("authors"))
        if authors is None or self._to_person(authors) is None:
            return []
        else:
            return [authors]

    @authors.setter
    def authors(self, authors: List[Union[Entity, Person]]) -> None:
        """Set the authors of the project."""
        authors = self._from_person(authors[0])
        self._set_property(self._get_key("authors"), authors)

    @staticmethod
    def _from_person(person: Union[Entity, Person]):
        """MkDocs Person is a string with full name."""
        return person.to_name_email_string()

    @staticmethod
    def _to_person(person: str) -> Optional[Union[Entity, Person]]:
        """MkDocs Person is a string with full name."""
        try:
            return Person.from_name_email_string(person)
        except (ValueError, AttributeError):
            logger.info(f"Cannot convert {person} to Person object, trying Entity.")

        try:
            return Entity.from_name_email_string(person)
        except (ValueError, AttributeError):
            logger.warning(f"Cannot convert {person} to Entity.")
            return None

    def sync(self, metadata: ProjectMetadata) -> None:
        """Sync the MkDocs object with the ProjectMetadata object."""
        self.name = metadata.name
        self.description = metadata.description
        # no author merge since it is a free text field
        self.authors = metadata.authors()
        if metadata.homepage:
            self.homepage = str(metadata.homepage)
        if metadata.repository:
            self.repository = str(metadata.repository)
            self.repo_name = metadata.repository.path
