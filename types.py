from dataclasses import dataclass


@dataclass
class ImportStatement:
    """Imports an external module."""
    module: str


@dataclass
class IncludeStatement:
    """Includes a local file or module."""
    module: str


@dataclass
class MainScope:
    """Outer container for the AST."""
    imports: list[ImportStatement]  #note: these are ordered here but they can be intermixed before compilation
    includes: list[IncludeStatement]


