#!/usr/bin/env python3
"""Generuje plik Excel (.xlsx) z milestone'ami projektu bez zewnętrznych bibliotek.

Przykład:
    python3 milestones_to_excel.py --input milestones_sample.csv --output harmonogram.xlsx
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from xml.sax.saxutils import escape
import zipfile


@dataclass
class Milestone:
    name: str
    owner: str
    start_date: str
    due_date: str
    status: str
    progress: int
    notes: str


HEADERS = [
    "Milestone",
    "Owner",
    "Start date",
    "Due date",
    "Status",
    "Progress (%)",
    "Notes",
]

# Style indexes from styles.xml
STYLE_HEADER = 1
STYLE_DATE = 2
STYLE_STATUS_TODO = 3
STYLE_STATUS_IN_PROGRESS = 4
STYLE_STATUS_DONE = 5
STYLE_STATUS_BLOCKED = 6

STATUS_STYLE_MAP: Dict[str, int] = {
    "TODO": STYLE_STATUS_TODO,
    "IN_PROGRESS": STYLE_STATUS_IN_PROGRESS,
    "DONE": STYLE_STATUS_DONE,
    "BLOCKED": STYLE_STATUS_BLOCKED,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Eksport milestone'ów do Excela")
    parser.add_argument("--input", required=True, help="Ścieżka do pliku CSV")
    parser.add_argument("--output", default="milestones.xlsx", help="Nazwa pliku XLSX")
    return parser.parse_args()


def validate_date(date_text: str) -> None:
    datetime.strptime(date_text, "%Y-%m-%d")


def parse_progress(raw: str) -> int:
    progress = int(raw)
    if not 0 <= progress <= 100:
        raise ValueError("Progress musi być w zakresie 0-100")
    return progress


def load_milestones(csv_path: Path) -> List[Milestone]:
    with csv_path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"name", "owner", "start_date", "due_date", "status", "progress", "notes"}
        missing = required.difference(reader.fieldnames or set())
        if missing:
            raise ValueError(f"Brakuje kolumn w CSV: {', '.join(sorted(missing))}")

        milestones: List[Milestone] = []
        for index, row in enumerate(reader, start=2):
            try:
                validate_date(row["start_date"])
                validate_date(row["due_date"])
                progress = parse_progress(row["progress"])
            except Exception as exc:
                raise ValueError(f"Błąd w wierszu {index}: {exc}") from exc

            milestones.append(
                Milestone(
                    name=row["name"].strip(),
                    owner=row["owner"].strip(),
                    start_date=row["start_date"].strip(),
                    due_date=row["due_date"].strip(),
                    status=row["status"].strip().upper(),
                    progress=progress,
                    notes=row["notes"].strip(),
                )
            )

    if not milestones:
        raise ValueError("Plik CSV nie zawiera żadnych milestone'ów")
    return milestones


def excel_col(col_index: int) -> str:
    result = ""
    while col_index > 0:
        col_index, remainder = divmod(col_index - 1, 26)
        result = chr(65 + remainder) + result
    return result


def excel_serial_date(date_text: str) -> int:
    """Converts YYYY-MM-DD to Excel serial date (1900 date system)."""
    date_obj = datetime.strptime(date_text, "%Y-%m-%d").date()
    excel_epoch = datetime(1899, 12, 30).date()
    return (date_obj - excel_epoch).days


def make_inline_str_cell(ref: str, value: str, style: int | None = None) -> str:
    style_attr = f' s="{style}"' if style is not None else ""
    return f'<c r="{ref}" t="inlineStr"{style_attr}><is><t>{escape(value)}</t></is></c>'


def make_number_cell(ref: str, value: int, style: int | None = None) -> str:
    style_attr = f' s="{style}"' if style is not None else ""
    return f'<c r="{ref}"{style_attr}><v>{value}</v></c>'


def estimate_column_widths(milestones: List[Milestone]) -> List[int]:
    widths = [len(header) for header in HEADERS]
    for milestone in milestones:
        values = [
            milestone.name,
            milestone.owner,
            milestone.start_date,
            milestone.due_date,
            milestone.status,
            str(milestone.progress),
            milestone.notes,
        ]
        for i, value in enumerate(values):
            widths[i] = max(widths[i], len(value))

    # Dajemy margines i limit, aby arkusz nie był ekstremalnie szeroki.
    return [min(max(width + 2, 10), 60) for width in widths]


def build_cols_xml(widths: List[int]) -> str:
    cols = []
    for i, width in enumerate(widths, start=1):
        cols.append(f'<col min="{i}" max="{i}" width="{width}" customWidth="1"/>')
    return f'<cols>{"".join(cols)}</cols>'


def build_sheet_xml(milestones: List[Milestone]) -> str:
    rows = []

    header_cells = [
        make_inline_str_cell(f"{excel_col(i)}1", header, STYLE_HEADER) for i, header in enumerate(HEADERS, start=1)
    ]
    rows.append('<row r="1" ht="22" customHeight="1">' + "".join(header_cells) + "</row>")

    for row_idx, milestone in enumerate(milestones, start=2):
        row_cells = [
            make_inline_str_cell(f"A{row_idx}", milestone.name),
            make_inline_str_cell(f"B{row_idx}", milestone.owner),
            make_number_cell(f"C{row_idx}", excel_serial_date(milestone.start_date), STYLE_DATE),
            make_number_cell(f"D{row_idx}", excel_serial_date(milestone.due_date), STYLE_DATE),
            make_inline_str_cell(
                f"E{row_idx}", milestone.status, STATUS_STYLE_MAP.get(milestone.status, STYLE_STATUS_TODO)
            ),
            make_number_cell(f"F{row_idx}", milestone.progress),
            make_inline_str_cell(f"G{row_idx}", milestone.notes),
        ]
        rows.append(f'<row r="{row_idx}">{"".join(row_cells)}</row>')

    last_row = len(milestones) + 1
    cols_xml = build_cols_xml(estimate_column_widths(milestones))
    sheet_data = "".join(rows)

    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        f"{cols_xml}"
        '<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>'
        '<sheetFormatPr defaultRowHeight="15"/>'
        f'<sheetData>{sheet_data}</sheetData>'
        f'<autoFilter ref="A1:G{last_row}"/>'
        '</worksheet>'
    )


def build_styles_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <numFmts count="1">
    <numFmt numFmtId="164" formatCode="yyyy-mm-dd"/>
  </numFmts>
  <fonts count="2">
    <font>
      <sz val="11"/>
      <color theme="1"/>
      <name val="Calibri"/>
      <family val="2"/>
    </font>
    <font>
      <b/>
      <sz val="11"/>
      <color rgb="FFFFFFFF"/>
      <name val="Calibri"/>
      <family val="2"/>
    </font>
  </fonts>
  <fills count="6">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="gray125"/></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FF4F81BD"/><bgColor indexed="64"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFFFF2CC"/><bgColor indexed="64"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFD9EAD3"/><bgColor indexed="64"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFF4CCCC"/><bgColor indexed="64"/></patternFill></fill>
  </fills>
  <borders count="1">
    <border><left/><right/><top/><bottom/><diagonal/></border>
  </borders>
  <cellStyleXfs count="1">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0"/>
  </cellStyleXfs>
  <cellXfs count="7">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
    <xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1"/>
    <xf numFmtId="164" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/>
    <xf numFmtId="0" fontId="0" fillId="3" borderId="0" xfId="0" applyFill="1"/>
    <xf numFmtId="0" fontId="0" fillId="3" borderId="0" xfId="0" applyFill="1"/>
    <xf numFmtId="0" fontId="0" fillId="4" borderId="0" xfId="0" applyFill="1"/>
    <xf numFmtId="0" fontId="0" fillId="5" borderId="0" xfId="0" applyFill="1"/>
  </cellXfs>
  <cellStyles count="1">
    <cellStyle name="Normal" xfId="0" builtinId="0"/>
  </cellStyles>
</styleSheet>"""


def write_xlsx(output_path: Path, milestones: List[Milestone]) -> None:
    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
</Types>"""

    root_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>"""

    workbook = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
          xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="Milestones" sheetId="1" r:id="rId1"/>
  </sheets>
</workbook>"""

    workbook_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""

    sheet_xml = build_sheet_xml(milestones)
    styles_xml = build_styles_xml()

    with zipfile.ZipFile(output_path, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", content_types)
        archive.writestr("_rels/.rels", root_rels)
        archive.writestr("xl/workbook.xml", workbook)
        archive.writestr("xl/_rels/workbook.xml.rels", workbook_rels)
        archive.writestr("xl/worksheets/sheet1.xml", sheet_xml)
        archive.writestr("xl/styles.xml", styles_xml)


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        raise FileNotFoundError(f"Nie znaleziono pliku wejściowego: {input_path}")

    milestones = load_milestones(input_path)
    write_xlsx(output_path, milestones)
    print(f"Zapisano: {output_path.resolve()}")


if __name__ == "__main__":
    main()
