"""
Data Testing: AI based tool for Early Stage Dementia Detection
Project ID: SKIT/AI/2023-2027/27

Validates dataset quality, labels and the train/validation split.

Usage:
    python data_testing.py
    python data_testing.py "D:\\path\\to\\dataset"

Outputs (written next to this script):
    data_testing_report.csv  - per-file details
    data_testing_report.md   - summary of all checks
"""
import sys
from datetime import date
from pathlib import Path

import pandas as pd
import soundfile as sf

BASE = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(r"D:\SKIT_Project\dataset")
CLASS_FOLDERS = ["dementia", "nodementia"]
TRAIN_CSV = BASE / "train_dm.csv"
VALID_CSV = BASE / "valid_dm.csv"
SHORT_CLIP_SEC = 10
OUT_DIR = Path(__file__).resolve().parent

results = []


def add(test_id, check, expected, actual, status):
    results.append((test_id, check, expected, str(actual), status))
    print(f"[{status}] {test_id} {check}: {actual}")


# Audio file checks
rows = []
for label in CLASS_FOLDERS:
    for f in (BASE / label).rglob("*.wav"):
        try:
            info = sf.info(str(f))
            rows.append({
                "file": f.name,
                "folder_label": label,
                "sample_rate": info.samplerate,
                "channels": info.channels,
                "duration_sec": round(info.duration, 2),
                "status": "OK",
            })
        except Exception as e:
            rows.append({
                "file": f.name,
                "folder_label": label,
                "sample_rate": None,
                "channels": None,
                "duration_sec": None,
                "status": f"CORRUPT: {e}",
            })

if not rows:
    sys.exit(f"No .wav files found under {BASE}. Check the dataset path.")

df = pd.DataFrame(rows)
df["speaker"] = df["file"].str.rsplit("_", n=1).str[0]
df.to_csv(OUT_DIR / "data_testing_report.csv", index=False)

counts = df["folder_label"].value_counts().to_dict()
total = len(df)
add("DT-01", "Total audio files", "> 0", f"{total} {counts}", "PASS")

corrupt = int((df["status"] != "OK").sum())
add("DT-02", "Corrupt or unreadable files", "0", corrupt, "PASS" if corrupt == 0 else "FAIL")

ok = df[df["status"] == "OK"]

sample_rates = ok["sample_rate"].unique().tolist()
add("DT-03", "Consistent sample rate", "1 unique value", sample_rates,
    "PASS" if len(sample_rates) == 1 else "WARN")

channels = ok["channels"].unique().tolist()
add("DT-04", "Consistent channel count", "1 unique value", channels,
    "PASS" if len(channels) == 1 else "WARN")

dup_names = int(df["file"].duplicated().sum())
add("DT-05", "Duplicate file names", "0", dup_names, "PASS" if dup_names == 0 else "FAIL")

short = int((ok["duration_sec"] < SHORT_CLIP_SEC).sum())
add("DT-06", f"Clips shorter than {SHORT_CLIP_SEC}s", "0",
    f"{short} (min={ok['duration_sec'].min()}s, max={ok['duration_sec'].max()}s, "
    f"mean={round(ok['duration_sec'].mean(), 2)}s)",
    "PASS" if short == 0 else "WARN")

if len(counts) == 2:
    minority_pct = round(min(counts.values()) / total * 100, 1)
    add("DT-07", "Class balance (minority class share)", ">= 40%", f"{minority_pct}%",
        "PASS" if minority_pct >= 40 else "WARN")

# CSV and label checks
known_stems = set(Path(f).stem for f in df["file"])
stem_to_folder = dict(zip(df["file"].map(lambda x: Path(x).stem), df["folder_label"]))


def detect_file_column(frame):
    best, best_score = None, 0
    for col in frame.columns:
        values = frame[col].dropna().astype(str)
        if values.empty:
            continue
        score = values.map(lambda v: Path(v).stem in known_stems).mean()
        if score > best_score:
            best, best_score = col, score
    return best


def load_csv(path, name):
    if not path.exists():
        add("DT-08", f"{name} available", "exists", f"not found: {path}", "SKIPPED")
        return None, None
    frame = pd.read_csv(path)
    return frame, detect_file_column(frame)


train, train_col = load_csv(TRAIN_CSV, "train_dm.csv")
valid, valid_col = load_csv(VALID_CSV, "valid_dm.csv")

for name, frame, fcol in [("train", train, train_col), ("valid", valid, valid_col)]:
    if frame is None:
        continue

    nulls = int(frame.isnull().sum().sum())
    add("DT-09", f"{name}: null values", "0", nulls, "PASS" if nulls == 0 else "FAIL")

    dups = int(frame.duplicated().sum())
    add("DT-10", f"{name}: duplicate rows", "0", dups, "PASS" if dups == 0 else "FAIL")

    if fcol is None:
        add("DT-11", f"{name}: file column detected", "found", "not found", "WARN")
        continue

    stems = frame[fcol].astype(str).map(lambda v: Path(v).stem)
    missing = int((~stems.isin(known_stems)).sum())
    add("DT-11", f"{name}: CSV entries present in dataset folders", "0 missing",
        f"{missing} missing", "PASS" if missing == 0 else "FAIL")

    label_cols = [c for c in frame.columns if c != fcol]
    if label_cols:
        tmp = pd.DataFrame({
            "folder": stems.map(stem_to_folder),
            "label": frame[label_cols[-1]],
        }).dropna(subset=["folder"])
        per_folder = tmp.groupby("folder")["label"].nunique()
        mapping = tmp.groupby("folder")["label"].agg(lambda s: s.mode().iloc[0])
        consistent = bool((per_folder == 1).all() and mapping.nunique() == len(mapping))
        add("DT-12", f"{name}: CSV label matches folder", "one distinct label per folder",
            mapping.to_dict() if consistent else f"mismatch {per_folder.to_dict()}",
            "PASS" if consistent else "FAIL")

if train is not None and valid is not None and train_col and valid_col:
    train_stems = set(train[train_col].astype(str).map(lambda v: Path(v).stem))
    valid_stems = set(valid[valid_col].astype(str).map(lambda v: Path(v).stem))

    overlap = len(train_stems & valid_stems)
    add("DT-13", "Train/validation file overlap", "0", overlap, "PASS" if overlap == 0 else "FAIL")

    def speakers(stems):
        return set(s.rsplit("_", 1)[0] for s in stems)

    speaker_overlap = len(speakers(train_stems) & speakers(valid_stems))
    add("DT-14", "Speakers present in both train and validation", "0", speaker_overlap,
        "PASS" if speaker_overlap == 0 else "WARN")

# Report
n_pass = sum(r[4] == "PASS" for r in results)
n_warn = sum(r[4] == "WARN" for r in results)
n_fail = sum(r[4] == "FAIL" for r in results)
n_skip = sum(r[4] == "SKIPPED" for r in results)

lines = [
    "# Data Testing Report",
    "",
    "**Project:** AI based tool for Early Stage Dementia Detection (SKIT/AI/2023-2027/27)  ",
    "**Tested by:** Narendra Choudhary  ",
    f"**Date:** {date.today().strftime('%d/%m/%Y')}  ",
    "**Scope:** Dataset quality, labels and train/validation split",
    "",
    "## Results",
    "",
    "| Test ID | Check | Expected | Actual | Status |",
    "|---|---|---|---|---|",
]
for tid, chk, exp, act, st in results:
    lines.append(f"| {tid} | {chk} | {exp} | {act} | {st} |")

lines += [
    "",
    f"**Summary:** {n_pass} passed, {n_warn} warnings, {n_fail} failed, {n_skip} skipped.",
    "",
    "## Observations",
    "",
]
flagged = [r for r in results if r[4] in ("WARN", "FAIL")]
if flagged:
    for tid, chk, exp, act, st in flagged:
        lines.append(f"- {tid} ({st}): {chk} - expected {exp}, found {act}.")
else:
    lines.append("- No issues found in any executed check.")

lines += ["", "## Conclusion", ""]
if n_fail:
    lines.append("The dataset has failed checks that must be fixed before model training.")
elif n_warn:
    lines.append("The dataset passed all critical checks. The warnings above should be noted during model training and evaluation.")
else:
    lines.append("The dataset passed all checks and is suitable for model training.")

lines += ["", "Per-file details are available in `data_testing_report.csv`."]
(OUT_DIR / "data_testing_report.md").write_text("\n".join(lines), encoding="utf-8")
print(f"\nReports saved in: {OUT_DIR}")
