"""
Model Testing on Unseen Data  --  Dementia Detection (Sprint: Testing, Evaluation & Documentation)
Owner: Narendra Choudhary | Task window: 9/10/26 - 7/11/26

Kya karta hai:
  1. dementia / nodementia folders se .wav files leta hai
  2. MFCC + spectral features nikalta hai (librosa)
  3. Data ko train / UNSEEN test me split karta hai (stratified, optional speaker-wise)
  4. Model load karta hai (Nishit ka .joblib) -- agar nahi hai to ek baseline train karta hai
  5. Unseen data par metrics nikalta hai: accuracy, precision, recall, F1, ROC-AUC, confusion matrix
  6. results/ folder me report, plots aur misclassified.csv save karta hai (Error Analysis sprint ke kaam aayega)

Run:
  python model_testing.py --root D:\\SKIT_Project\\dataset
  python model_testing.py --root D:\\SKIT_Project\\dataset --model nishit_model.joblib
"""
import argparse
import json
import warnings
from pathlib import Path

import joblib
import librosa
import matplotlib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    ConfusionMatrixDisplay, RocCurveDisplay, accuracy_score, classification_report,
    confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score,
)
from sklearn.model_selection import GroupShuffleSplit, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

warnings.filterwarnings("ignore")
CLASS_FOLDERS = {"nodementia": 0, "dementia": 1}  # 1 = dementia (positive class)
SR = 16000


def extract_features(path: Path) -> np.ndarray:
    """MFCC(13) mean+std, delta MFCC mean, spectral features, ZCR, RMS -> fixed-length vector."""
    y, sr = librosa.load(path, sr=SR, mono=True)
    y, _ = librosa.effects.trim(y, top_db=25)
    if len(y) < sr // 2:  # bahut chhoti clip
        y = np.pad(y, (0, sr // 2 - len(y)))
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    delta = librosa.feature.delta(mfcc)
    cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    roll = librosa.feature.spectral_rolloff(y=y, sr=sr)
    zcr = librosa.feature.zero_crossing_rate(y)
    rms = librosa.feature.rms(y=y)
    feats = [mfcc.mean(1), mfcc.std(1), delta.mean(1)]
    for m in (cent, roll, zcr, rms):
        feats.append([m.mean(), m.std()])
    feats.append([len(y) / sr])  # duration
    return np.concatenate([np.ravel(f) for f in feats])


def build_dataset(root: Path, cache: Path) -> pd.DataFrame:
    if cache.exists():
        print(f"[cache] {cache} se features load kiye")
        return pd.read_pickle(cache)
    rows = []
    for folder, label in CLASS_FOLDERS.items():
        files = sorted((root / folder).rglob("*.wav"))
        print(f"{folder}: {len(files)} files")
        for f in files:
            try:
                rows.append({"file": str(f), "label": label, "feat": extract_features(f)})
            except Exception as e:  # corrupt audio ko skip karo, par log karo
                print(f"  [skip] {f.name}: {e}")
    df = pd.DataFrame(rows)
    if df.empty:
        raise SystemExit("Koi .wav file nahi mili. --root path check karo.")
    df.to_pickle(cache)
    return df


def split_unseen(df, test_size, seed, group_regex):
    """Unseen test set. Agar filename se speaker id nikal sakte ho to speaker-wise split (no leakage)."""
    idx = np.arange(len(df))
    if group_regex:
        groups = df["file"].map(lambda p: Path(p).stem).str.extract(group_regex)[0].fillna(df["file"])
        gss = GroupShuffleSplit(n_splits=1, test_size=test_size, random_state=seed)
        tr, te = next(gss.split(idx, df["label"], groups))
        print(f"Speaker-wise split use hua ({groups.nunique()} unique speakers)")
    else:
        tr, te = train_test_split(idx, test_size=test_size, stratify=df["label"], random_state=seed)
        print("WARNING: random split. Agar ek hi speaker ki multiple clips hain to leakage ho sakti hai; --group-regex use karo.")
    if len(set(df["label"].values[te])) < 2:
        print("WARNING: test set me sirf ek class hai -- seed/test-size badlo, metrics misleading honge.")
    return tr, te


def evaluate(model, X_te, y_te, out: Path, files_te):
    y_pred = model.predict(X_te)
    y_prob = model.predict_proba(X_te)[:, 1] if hasattr(model, "predict_proba") else None
    m = {
        "n_test": int(len(y_te)),
        "accuracy": accuracy_score(y_te, y_pred),
        "precision": precision_score(y_te, y_pred, zero_division=0),
        "recall_sensitivity": recall_score(y_te, y_pred, zero_division=0),
        "f1": f1_score(y_te, y_pred, zero_division=0),
    }
    tn, fp, fn, tp = confusion_matrix(y_te, y_pred, labels=[0, 1]).ravel()
    m.update(specificity=tn / (tn + fp) if (tn + fp) else float("nan"), TP=int(tp), TN=int(tn), FP=int(fp), FN=int(fn))
    if y_prob is not None and len(set(y_te)) == 2:
        m["roc_auc"] = roc_auc_score(y_te, y_prob)
        RocCurveDisplay.from_predictions(y_te, y_prob)
        plt.title("ROC - unseen test data"); plt.savefig(out / "roc_curve.png", dpi=150, bbox_inches="tight"); plt.close()
    ConfusionMatrixDisplay.from_predictions(y_te, y_pred, labels=[0, 1], display_labels=["No dementia", "Dementia"], cmap="Blues")
    plt.title("Confusion matrix - unseen test data"); plt.savefig(out / "confusion_matrix.png", dpi=150, bbox_inches="tight"); plt.close()

    wrong = pd.DataFrame({"file": files_te, "true": y_te, "pred": y_pred,
                          "prob_dementia": y_prob if y_prob is not None else np.nan})
    wrong = wrong[wrong.true != wrong.pred]
    wrong["error_type"] = np.where(wrong.pred == 1, "False Positive", "False Negative")
    wrong.to_csv(out / "misclassified.csv", index=False)

    report = classification_report(y_te, y_pred, labels=[0, 1], target_names=["No dementia", "Dementia"], zero_division=0)
    (out / "metrics.json").write_text(json.dumps({k: float(v) for k, v in m.items()}, indent=2))
    md = ["# Model Testing Report (Unseen Data)", "", "| Metric | Value |", "|---|---|"]
    md += [f"| {k} | {v:.4f} |" if isinstance(v, float) else f"| {k} | {v} |" for k, v in m.items()]
    md += ["", "```", report, "```", "",
           f"Misclassified: {len(wrong)} (FP={fp}, FN={fn}). Detail: misclassified.csv",
           "", "Note: medical screening me **recall (FN kam rakhna)** accuracy se zyada important hai."]
    (out / "test_report.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="folder jisme dementia/ aur nodementia/ hain")
    ap.add_argument("--model", help="saved sklearn model/pipeline (.joblib). Na do to baseline train hoga")
    ap.add_argument("--test-size", type=float, default=0.2)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--group-regex", default=None, help=r"filename se speaker id regex, e.g. '^(\w+?)_'")
    ap.add_argument("--out", default="results")
    a = ap.parse_args()

    out = Path(a.out); out.mkdir(exist_ok=True)
    df = build_dataset(Path(a.root), out / "features_cache.pkl")
    X, y = np.vstack(df["feat"].values), df["label"].values
    tr, te = split_unseen(df, a.test_size, a.seed, a.group_regex)

    if a.model:
        model = joblib.load(a.model)
        print(f"Loaded model: {a.model}  (NOTE: iska feature format wahi hona chahiye jo yahan extract hota hai)")
    else:
        model = make_pipeline(StandardScaler(), RandomForestClassifier(300, class_weight="balanced", random_state=a.seed))
        model.fit(X[tr], y[tr])
        joblib.dump(model, out / "baseline_model.joblib")
        print("Baseline RandomForest train hua (sirf pipeline verify karne ke liye)")

    evaluate(model, X[te], y[te], out, df["file"].values[te])


if __name__ == "__main__":
    main()
