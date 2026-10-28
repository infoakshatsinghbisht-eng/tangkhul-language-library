"""Configuration management and standard paths for Tangkhul Language Library."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class LibraryPaths:
    """Standard filesystem paths used by the library."""

    root_dir: Path
    data_dir: Path = field(init=False)
    manifests_dir: Path = field(init=False)
    raw_dir: Path = field(init=False)
    processed_dir: Path = field(init=False)
    exports_dir: Path = field(init=False)
    package_dir: Path = field(init=False)
    package_data_dir: Path = field(init=False)

    def __post_init__(self) -> None:
        data = self.root_dir / "data"
        pkg = Path(__file__).resolve().parent.parent
        object.__setattr__(self, "data_dir", data)
        object.__setattr__(self, "manifests_dir", data / "manifests")
        object.__setattr__(self, "raw_dir", data / "raw")
        object.__setattr__(self, "processed_dir", data / "processed")
        object.__setattr__(self, "exports_dir", data / "exports")
        object.__setattr__(self, "database_dir", data / "database")
        object.__setattr__(self, "package_dir", pkg)
        object.__setattr__(self, "package_data_dir", pkg / "data")


@dataclass
class LibraryConfig:
    """Global configuration settings for Tangkhul Language Library."""

    paths: LibraryPaths
    default_language: str = "Tangkhul"
    sqlite_db_name: str = "tangkhul_corpus.sqlite"

    def get_database_path(self) -> Path:
        """Return path to active SQLite database, falling back to bundled package database."""
        db_path = self.paths.database_dir / self.sqlite_db_name
        if db_path.is_file():
            return db_path
        bundled_db = self.paths.package_data_dir / self.sqlite_db_name
        if bundled_db.is_file():
            return bundled_db
        return db_path

    @classmethod
    def find_project_root(cls, start_path: Path | None = None) -> Path:
        """Locate project root by searching upwards for pyproject.toml."""
        current = (start_path or Path.cwd()).resolve()
        for parent in [current, *current.parents]:
            if (parent / "pyproject.toml").is_file():
                return parent
        # Fallback to current directory if pyproject.toml is not found
        return current

    @classmethod
    def from_environment(cls) -> LibraryConfig:
        """Create configuration detecting project root or using environment variables."""
        env_root = os.environ.get("TANGKHUL_ROOT")
        root = Path(env_root).resolve() if env_root else cls.find_project_root()
        return cls(paths=LibraryPaths(root_dir=root))


def get_config() -> LibraryConfig:
    """Return standard LibraryConfig instance initialized from environment or project root."""
    return LibraryConfig.from_environment()

