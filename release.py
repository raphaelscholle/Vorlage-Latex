#!/usr/bin/env python3
"""Build and package a dated TMDT thesis-template release."""

from __future__ import annotations

import subprocess
import sys
from datetime import date
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parent
ARCHIVE = ROOT / f"TMDT-Thesisvorlage_{date.today().isoformat()}.zip"
FILES = (
    "Thesis.tex",
    "Einstellungen.tex",
    "siunitx.cfg",
    "README.md",
    "build.py",
)
DIRECTORIES = ("Kapitel", "Medien", "Verzeichnisse", "Vorlage")


def main() -> int:
    build = subprocess.run([sys.executable, str(ROOT / "build.py")], cwd=ROOT)
    if build.returncode != 0:
        return build.returncode

    with ZipFile(ARCHIVE, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for filename in FILES:
            archive.write(ROOT / filename, filename)
        archive.write(ROOT / "Thesis.pdf", "Thesisbeispiel-FAQ-Tipps.pdf")
        for directory in DIRECTORIES:
            for path in sorted((ROOT / directory).rglob("*")):
                if path.is_file():
                    archive.write(path, path.relative_to(ROOT))

    print(f"Release erstellt: {ARCHIVE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
