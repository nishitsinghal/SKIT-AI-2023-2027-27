
"""
Generate consolidated team contribution report from weekly PDFs.
"""

import datetime
import html
import re
import sys
from pathlib import Path
from collections import defaultdict

from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, LongTable, TableStyle
)


BASE_DIR = Path(__file__).resolve().parent
WEEKLY_REPORT_DIR = BASE_DIR / "weekly_reports"

MAX_REPORTS = 10
MIN_REPORTS = 9
DISPLAY_WEEKS = 9

STUDENT_HEADER = re.compile(
    r"^Student:\s*(.*?)\s+(?:—|–|-|�)\s+(\d+)\s+commit\(s\)\s*$"
)

DATE_LINE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
HASH_LINE = re.compile(r"^[0-9a-f]{7,40}$", re.IGNORECASE)


def check_weekly_reports():

    if not WEEKLY_REPORT_DIR.exists():
        raise FileNotFoundError("weekly_reports folder not found.")

    reports = sorted(
        report for report in WEEKLY_REPORT_DIR.glob(
            "*_Weekly_Progress_Report_Form-3_*.pdf"
        )
        if "_Combined_Weekly_Progress_Report_Form-3_" not in report.name
    )

    # Use the latest 10 weekly PDF reports.
    reports = reports[-MAX_REPORTS:]

    print("Weekly reports selected:", len(reports))

    for report in reports:
        print("-", report.name)

    if len(reports) < MIN_REPORTS:
        raise ValueError(
            f"At least {MIN_REPORTS} weekly reports are required. "
            f"Found only {len(reports)}."
        )

    return reports


def extract_student_logs(report):

    reader = PdfReader(str(report))
    lines = []

    for page in reader.pages:
        lines.extend((page.extract_text() or "").splitlines())

    logs = []
    current_student = None
    commit_date = None
    commit_hash = None
    message_parts = []
    expected_commits = None
    current_commit_count = 0
    found_log_section = False

    def save_commit():
        nonlocal current_commit_count

        if commit_date and commit_hash and current_student:
            message = " ".join(message_parts).strip()
            if not message:
                message = "(No commit message)"

            logs.append((
                current_student,
                commit_date,
                commit_hash,
                message
            ))

            current_commit_count += 1

    def finish_student():
        save_commit()

        if (
            current_student
            and expected_commits is not None
            and current_commit_count != expected_commits
        ):
            raise ValueError(
                f"{report.name}: Commit count mismatch for "
                f"{current_student}. Expected {expected_commits}, "
                f"found {current_commit_count}."
            )

    for raw_line in lines:

        line = raw_line.strip()

        if line.startswith("3. Detailed Commit Logs"):
            found_log_section = True
            continue

        if not found_log_section:
            continue

        if line == "No commit logs found for this timeframe.":
            continue

        student_match = STUDENT_HEADER.match(line)

        if student_match:
            finish_student()

            current_student = student_match.group(1).strip()
            expected_commits = int(student_match.group(2))
            current_commit_count = 0
            commit_date = None
            commit_hash = None
            message_parts = []
            continue

        if line.startswith("Name:"):
            finish_student()
            current_student = None
            expected_commits = None
            current_commit_count = 0
            commit_date = None
            commit_hash = None
            message_parts = []
            continue

        if not current_student:
            continue

        if line in {
            "Date", "Hash", "Commit Message", "Mentor Marks (/10)"
        }:
            continue

        if re.match(r"^_+\s*/\s*10$", line):
            continue

        if DATE_LINE.match(line):
            save_commit()
            commit_date = line
            commit_hash = None
            message_parts = []

        elif commit_date and commit_hash is None and HASH_LINE.match(line):
            commit_hash = line

        elif commit_date and commit_hash:
            message_parts.append(line)

    finish_student()

    if not found_log_section:
        raise ValueError(
            f"{report.name} has no Detailed Commit Logs section."
        )

    return logs


def collect_student_logs(reports):

    logs_by_student = {}
    seen_commits = defaultdict(set)
    display_names = {}

    for report in reports:

        print("Reading:", report.name)

        for name, date, commit_hash, message in extract_student_logs(report):

            student_key = name.casefold()
            display_name = display_names.setdefault(
                student_key, name
            )

            # Avoid counting the same commit more than once.
            if commit_hash in seen_commits[student_key]:
                continue

            seen_commits[student_key].add(commit_hash)

            logs_by_student.setdefault(display_name, []).append(
                (date, commit_hash, message)
            )

    return {
        student: sorted(
            logs, key=lambda item: (item[0], item[1])
        )
        for student, logs in sorted(
            logs_by_student.items(),
            key=lambda item: item[0].casefold()
        )
    }


def create_report(reports):

    logs_by_student = collect_student_logs(reports)

    stamp = datetime.date.today().strftime("%Y-%m-%d")

    output_path = WEEKLY_REPORT_DIR / (
        f"{BASE_DIR.name}_Combined_Weekly_Progress_Report_Form-3_"
        f"{stamp}.pdf"
    )

    document = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Normal"],
        fontSize=9,
        textColor=colors.HexColor("#64748B"),
        spaceAfter=12
    )

    student_style = ParagraphStyle(
        "StudentHeading",
        parent=styles["Heading2"],
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#1D4ED8"),
        spaceBefore=12,
        spaceAfter=5,
        keepWithNext=True
    )

    message_style = ParagraphStyle(
        "CommitMessage",
        parent=styles["BodyText"],
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#1E293B")
    )

    cell_style = ParagraphStyle(
        "CommitCell",
        parent=styles["BodyText"],
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#475569")
    )

    story = [
        Paragraph(
            "Project Contributions by Team Member",
            title_style
        ),

        Paragraph(
            f"Consolidated from {DISPLAY_WEEKS} Weeks of "
            f"project contributions &nbsp;|&nbsp; "
            f"Generated {datetime.date.today():%B %d, %Y}",
            subtitle_style
        )
    ]

    # Overall contribution summary.
    summary_data = [["Team member", "Commits"]]

    for student, logs in logs_by_student.items():
        summary_data.append([student, str(len(logs))])

    if not logs_by_student:
        summary_data.append(["No commit logs found", "0"])

    summary_table = Table(
        summary_data,
        colWidths=[390, 100]
    )

    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E293B")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ALIGN", (1, 0), (1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#F8FAFC")]),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5)
    ]))

    story.extend([summary_table, Spacer(1, 10)])

    # Individual contribution details.
    for student, logs in logs_by_student.items():

        story.append(
            Paragraph(
                f"{html.escape(student)} - {len(logs)} commit(s)",
                student_style
            )
        )

        table_data = [[
            "Date",
            "Commit",
            "Work / commit message"
        ]]

        for commit_date, commit_hash, message in logs:

            table_data.append([
                Paragraph(html.escape(commit_date), cell_style),
                Paragraph(html.escape(commit_hash), cell_style),
                Paragraph(html.escape(message), message_style)
            ])

        commit_table = LongTable(
            table_data,
            colWidths=[75, 65, 350],
            repeatRows=1
        )

        commit_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#475569")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1),
             [colors.white, colors.HexColor("#F8FAFC")]),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 5)
        ]))

        story.append(commit_table)

    document.build(story)

    print("\nFinal report created successfully!")
    print("Location:", output_path)

    return output_path


def main():

    print("=" * 55)
    print("FINAL TEAM CONTRIBUTION REPORT")
    print("=" * 55)

    try:
        reports = check_weekly_reports()
        create_report(reports)

        print("\nREPORT GENERATED SUCCESSFULLY!")

    except Exception as error:
        print("\nERROR:", str(error))
        sys.exit(1)


if __name__ == "__main__":
    main()
