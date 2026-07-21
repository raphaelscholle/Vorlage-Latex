#!/usr/bin/env python3
"""Build the thesis on Windows and Linux and write Thesis.pdf."""

from __future__ import annotations

import shutil
import subprocess
import sys
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WORK = ROOT / ".build"
SOURCE = WORK / "source"
OUTPUT = WORK / "output"
PDF = ROOT / "Thesis.pdf"


# This checkout contains an old release archive whose contents were flattened and
# shifted by one file name.  Keep that historical input untouched and assemble the
# directory layout expected by the TeX sources in the private build directory.
LEGACY_LAYOUT = {
    "Thesis.tex": "verifyReleasePackage.sh",
    "Einstellungen.tex": "readme.txt",
    "siunitx.cfg": "Thesis.tex",
    "Vorlage/Praeambel.tex": "createReleasePackage.sh",
    "Vorlage/FrontMatter.tex": "Praeambel.tex",
    "Vorlage/BackMatter.tex": "FrontMatter.tex",
    "Kapitel/Einleitung.tex": "FAQ.tex",
    "Kapitel/Grundlagen.tex": "LaTeX-Beispiele.tex",
    "Kapitel/Entwurf.tex": "Grundlagen.tex",
    "Kapitel/Realisierung.tex": "Schlussbetrachtungen.tex",
    "Kapitel/Analyse.tex": "Einleitung.tex",
    "Kapitel/Schlussbetrachtungen.tex": "Zusatzerklaerung.tex",
    "Kapitel/Sourcecode.tex": "Aufgabenstellung.pdf",
    "Kapitel/Schaltplan.tex": "Sourcecode.tex",
    "Kapitel/Messreihen.tex": "Schaltplan.tex",
    "Kapitel/Kurzfassung.tex": "Messreihen.tex",
    "Kapitel/FAQ.tex": "Kurzfassung.tex",
    "Kapitel/LaTeX-Beispiele.tex": "Realisierung.tex",
    "Kapitel/Danksagung.tex": "Entwurf.tex",
    "Kapitel/DeclarationGenerativeAI.tex": "DeclarationGenerativeAI.tex",
    "Kapitel/Zusatzerklaerung.tex": "bestueckungbottom.png",
    "Medien/Aufgabenstellung.pdf": "Muster_Eidesstattliche_Versicherung.pdf",
    "Medien/Muster_Eidesstattliche_Versicherung.pdf": "schaltplan2.png",
    "Medien/Muster_Sperrvermerk_Thesis.pdf": "schaltplan3.png",
    "Medien/Verlaengerung.pdf": "Muster_Eidesstattliche_Versicherung.pdf",
    "Medien/bestueckungtop.png": "Muster_Sperrvermerk_Thesis.pdf",
    "Medien/bestueckungbottom.png": "schaltplan1.png",
    "Medien/schaltplan1.png": "schaltplan4.png",
    "Medien/schaltplan2.png": "suzanne-albedo.png",
    "Medien/schaltplan3.png": "suzanne-false-color.png",
    "Medien/schaltplan4.png": "suzanne-intensity.png",
    "Medien/suzanne-albedo.png": "suzanne-raw.png",
    "Medien/suzanne-false-color.png": "suzanne-sw.png",
    "Medien/suzanne-intensity.png": "suzanne-variance.png",
    "Medien/suzanne-raw.png": "Uni_Wuppertal_Logo.pdf",
    "Medien/suzanne-sw.png": "Uni_Wuppertal_Logo.sla",
    "Medien/suzanne-variance.png": "Uni_Wuppertal_Logo__cmykblack.pdf",
    "Medien/Uni_Wuppertal_Logo.pdf": "Uni_Wuppertal_Logo__rgbblack.pdf",
    "Medien/Uni_Wuppertal_Logo__cmykblack.pdf": "Uni_Wuppertal_Logo__rgbblack.pdf",
    "Medien/Uni_Wuppertal_Logo__rgbblack.pdf": "Uni_Wuppertal_Logo__rgbblack.pdf",
    "Medien/Uni_Wuppertal_Logo__richblack.pdf": "Uni_Wuppertal_Logo__rgbblack.pdf",
}


def is_regular_layout() -> bool:
    thesis = ROOT / "Thesis.tex"
    if not thesis.is_file():
        return False
    return "\\begin{document}" in thesis.read_text(encoding="utf-8", errors="ignore")


def prepare_source() -> Path:
    if is_regular_layout():
        return ROOT

    if not (ROOT / "verifyReleasePackage.sh").is_file():
        raise RuntimeError("Thesis.tex wurde nicht gefunden oder ist keine LaTeX-Hauptdatei.")

    shutil.rmtree(SOURCE, ignore_errors=True)
    for destination, origin in LEGACY_LAYOUT.items():
        source = ROOT / origin
        if not source.is_file():
            raise RuntimeError(f"Benötigte Quelldatei fehlt: {origin}")
        target = SOURCE / destination
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)

    # These two example databases are absent from the flattened archive. Supply
    # the entries referenced by the bundled example chapter.
    directories = SOURCE / "Verzeichnisse"
    directories.mkdir(parents=True, exist_ok=True)
    (directories / "Glossar.tex").write_text(
        r"""\newacronym{crc}{CRC}{Cyclic Redundancy Check}
\newacronym{svm}{SVM}{Support Vector Machine}
\newabbreviation{bspw}{bspw.}{beispielsweise}
\newglossaryentry{ex}{name={Beispiel},description={Ein beispielhafter Glossareintrag}}
\newglossaryentry{rekursion}{name={Rekursion},description={Selbstbezügliche Definition oder Verarbeitung}}
\newglossaryentry{labelname}{name={Name},description={Beispiel für einen Glossareintrag}}
\newglossaryentry{alpha}{type=symbols,name={Alpha},symbol={\ensuremath{\alpha}},description={Griechischer Buchstabe Alpha}}
\newglossaryentry{beta}{type=symbols,name={Beta},symbol={\ensuremath{\beta}},description={Griechischer Buchstabe Beta}}
\newglossaryentry{gamma}{type=symbols,name={Gamma},symbol={\ensuremath{\gamma}},description={Griechischer Buchstabe Gamma}}
\newglossaryentry{emptyset}{type=symbols,name={Leere Menge},symbol={\ensuremath{\emptyset}},description={Leere Menge}}
""",
        encoding="utf-8",
    )
    (directories / "Literatur.bib").write_text(
        r"""@misc{thesis:vorlage, author={Mustermann, Max}, title={Thesisvorlage}, year={2026}}
@manual{ARM:AMBA4AXI4StreamProtocol:v1_0, author={{Arm Ltd.}}, title={AMBA AXI4-Stream Protocol}, year={2021}}
@manual{Datenblatt:LD1117, author={{STMicroelectronics}}, title={LD1117 Datasheet}, year={2021}}
@misc{ADATspec96khz, author={{Alesis}}, title={ADAT Specification}, year={2001}}
@manual{AnalogDevices:MT-085, author={{Analog Devices}}, title={MT-085}, year={2009}}
@misc{literaturname, author={Mustermann, Max}, title={Beispielquelle}, year={2026}}
""",
        encoding="utf-8",
    )
    return SOURCE


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
        print("Fehler: pdflatex und bibtex8 wurden nicht gefunden. Bitte TeX Live oder MiKTeX installieren.", file=sys.stderr)
        return 2

    try:
        source = prepare_source()
    except (OSError, RuntimeError) as error:
        print(f"Fehler: {error}", file=sys.stderr)
        return 2

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
        # MiKTeX installations are frequently minimal. This lets MiKTeX fetch a
        # missing package instead of stopping at an interactive file-name prompt.
        latex_command.append("-enable-installer")
    latex_command.extend([
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
        f"-output-directory={OUTPUT}",
        "Thesis.tex",
    ])
    # pdflatex needs one pass for the aux data, BibTeX one pass for references,
    # and pdflatex two more passes for citations, page numbers and the TOC.
    commands = [latex_command, [bibtex, "Thesis"], latex_command, latex_command]
    logs = []
    environment = os.environ.copy()
    environment["BIBINPUTS"] = (
        str(source)
        + os.pathsep
        + str(source / "Verzeichnisse")
        + os.pathsep
        + environment.get("BIBINPUTS", "")
    )
    for index, command in enumerate(commands):
        cwd = OUTPUT if index == 1 else source
        result = subprocess.run(
            command,
            cwd=cwd,
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
