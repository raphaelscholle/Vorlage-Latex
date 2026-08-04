#!/usr/bin/env python3
"""Build the TMDT thesis template on Windows and Linux."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / ".build" / "output"
PDF = ROOT / "Thesis.pdf"


def prepare_miktex() -> None:
    """Initialize a minimal MiKTeX installation when biblatex is incomplete."""
    kpsewhich = shutil.which("kpsewhich")
    miktex = shutil.which("miktex")
    if kpsewhich is None or miktex is None:
        return
    present = subprocess.run(
        [kpsewhich, "logreq.sty"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if present.returncode == 0:
        return
    subprocess.run(
        [miktex, "packages", "update-package-database"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    subprocess.run(
        [miktex, "packages", "require", "logreq"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def main() -> int:
    pdflatex = shutil.which("pdflatex")
    bibtex = shutil.which("bibtex8") or shutil.which("bibtex")
    if pdflatex is None or bibtex is None:
        print(
            "Fehler: pdflatex und bibtex8 oder bibtex wurden nicht gefunden. "
            "Bitte TeX Live oder MiKTeX installieren.",
            file=sys.stderr,
        )
        return 2
    if not (ROOT / "Thesis.tex").is_file():
        print("Fehler: Thesis.tex wurde nicht gefunden.", file=sys.stderr)
        return 2

    # Auxiliary files contain paths and macro state from previous runs. Starting
    # clean avoids hard-to-diagnose failures after template or layout updates.
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    version = subprocess.run(
        [pdflatex, "--version"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="utf-8",
        errors="replace",
    ).stdout
    latex_command = [pdflatex]
    if "MiKTeX" in version:
        prepare_miktex()
        latex_command.append("-enable-installer")
    latex_command.extend(
        [
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-file-line-error",
            f"-output-directory={OUTPUT}",
            "Thesis.tex",
        ]
    )

    commands = [latex_command, [bibtex, "Thesis"], latex_command, latex_command]
    environment = os.environ.copy()
    environment["BIBINPUTS"] = (
        str(ROOT)
        + os.pathsep
        + str(ROOT / "Verzeichnisse")
        + os.pathsep
        + environment.get("BIBINPUTS", "")
    )
    logs: list[str] = []
    for index, command in enumerate(commands):
        working_directory = OUTPUT if index == 1 else ROOT
        result = subprocess.run(
            command,
            cwd=working_directory,
            env=environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="utf-8",
            errors="replace",
        )
        logs.append(result.stdout)
        if result.returncode != 0:
            print("".join(logs).rstrip(), file=sys.stderr)
            print("\nFehler: Die PDF konnte nicht gebaut werden.", file=sys.stderr)
            return result.returncode

    built_pdf = OUTPUT / "Thesis.pdf"
    if not built_pdf.is_file():
        print("".join(logs).rstrip(), file=sys.stderr)
        print("\nFehler: Die PDF konnte nicht gebaut werden.", file=sys.stderr)
        return 1

    shutil.copyfile(built_pdf, PDF)
    print(f"Erstellt: {PDF}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
