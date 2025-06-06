# Changelog

Here we provide notes that summarize the most important changes in each released version.

Please consult the changelog to inform yourself about breaking changes and security issues.

## [v0.7.3](https://github.com/Materials-Data-Science-and-Informatics/somesy/tree/v0.7.3) <small>(2025-03-14)</small> { id="0.7.3" }

- accept orcid id as string without url
- support multiline description in somesy input and outputs that enables multiline strings
- dont save same person in available output formats
- better toml inline table formatting
- support only orcid id string (without the url)

## [v0.7.2](https://github.com/Materials-Data-Science-and-Informatics/somesy/tree/v0.7.2) <small>(2025-03-10)</small> { id="0.7.2" }

- fix CITATION.CFF formatting
- fix codemeta.json missing maintainer property
- fix somesy model validator missing return

## [v0.7.1](https://github.com/Materials-Data-Science-and-Informatics/somesy/tree/v0.7.1) <small>(2025-03-07)</small> { id="0.7.1" }

- fix poetry v2 license format and urls format problem

## [v0.7.0](https://github.com/Materials-Data-Science-and-Informatics/somesy/tree/v0.7.0) <small>(2025-03-04)</small> { id="0.7.0" }

- make validation of output files, such as pyproject.toml, optional
- make somesy project metadata input `version` optional
- multiple output file support
- enable having packages support
- fix: package.json url set error on None value
- support poetry version 2

## [v0.6.0](https://github.com/Materials-Data-Science-and-Informatics/somesy/tree/v0.6.0) <small>(2025-02-14)</small> { id="0.6.0" }

- implement CFF Entity (Organization) model for author/maintainer/contributor
- add a new config option to use existing codemeta.json when syncing
- fix SomesyBaseModel kwargs being overwritten

## [v0.5.0](https://github.com/Materials-Data-Science-and-Informatics/somesy/tree/v0.5.0) <small>(2025-01-15)</small> { id="0.5.0" }

- make person (and entity) argument email optional

## [v0.4.3](https://github.com/Materials-Data-Science-and-Informatics/somesy/tree/v0.4.3) <small>(2024-07-29)</small> { id="0.4.3" }

- update python dependencies
- update pre-commit hook versions
- fix package.json person validation
- update poetry, julia, and package.json person validation: entries without an email wont't raise an error, they will be ignored.

## [v0.4.2](https://github.com/Materials-Data-Science-and-Informatics/somesy/tree/v0.4.2) <small>(2024-04-30)</small> { id="0.4.2" }

- fix rich logging bug for error messages and tracebacks

## [v0.4.1](https://github.com/Materials-Data-Science-and-Informatics/somesy/tree/v0.4.1) <small>(2024-04-08)</small> { id="0.4.1" }

- fix package.json and mkdocs.yml validation bug about optional fields

## [v0.4.0](https://github.com/Materials-Data-Science-and-Informatics/somesy/tree/v0.4.0) <small>(2024-03-08)</small> { id="0.4.0" }

- added separate `documentation` URL to Project metadata model
- added support for Julia `Project.toml` file
- added support for Fortran `fpm.toml` file
- added support for Java `pom.xml` file
- added support for MkDocs `mkdocs.yml` file
- added support for Rust `Cargo.toml` file

## [v0.3.1](https://github.com/Materials-Data-Science-and-Informatics/somesy/tree/v0.3.1) <small>(2024-01-23)</small> { id="0.3.1" }

- fix setuptools license writing bug

## [v0.3.0](https://github.com/Materials-Data-Science-and-Informatics/somesy/tree/v0.3.0) <small>(2024-01-12)</small> { id="0.3.0" }

- replace codemetapy with an in-house writer, which enables windows support

## [v0.2.1](https://github.com/Materials-Data-Science-and-Informatics/somesy/tree/v0.2.1) <small>(2023-11-29)</small> { id="0.2.1" }

- **internal:** updated linters and dependencies
- **internal:** pin codemetapy version to 2.5.2 to avoid breaking changes
- fix bug caused by missing `config` section

## [v0.2.0](https://github.com/Materials-Data-Science-and-Informatics/somesy/tree/v0.2.0) <small>(2023-11-29)</small> { id="0.2.0" }

- **internal:** Test refactoring
- **internal:** Pydantic 2 implementation
- Added `publication_author` field to Person model

## [v0.1.0](https://github.com/Materials-Data-Science-and-Informatics/somesy/tree/v0.1.0) <small>(2023-08-10)</small> { id="0.1.0" }

- First release
