"""Shim package so `python -m space_invaders` works from repository root."""

from pathlib import Path

__path__ = list(__path__)  # type: ignore[name-defined]
_src_pkg = Path(__file__).resolve().parent.parent / "src" / "space_invaders"
if _src_pkg.exists():
    __path__.append(str(_src_pkg))
