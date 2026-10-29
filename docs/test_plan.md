# Test Plan: AI-Based Tool for Early-Stage Dementia Detection

**Project ID:** SKIT/AI/2023-2027/27  
**Branch:** CSE (AI), Section B, Session 2026-27  
**Prepared by:** Narendra Choudhary (Testing, Evaluation & Documentation)  
**Team:** Vaibhav Kumar Jain (Frontend + Node.js backend, Team Lead), Nishit Singhal (AI/ML model), Sujal Solanki (NLP & speech processing)  
**Approved by:** Kapil Sharma (22/08/2026)  
**Last updated:** 29 October 2026

## 1. Objective
Verify that the dataset, ML model, and complete web system (frontend, backend, API, model) work correctly and reliably for detecting early-stage dementia from voice recordings.

## 2. Scope
| Area | What is tested | Sprint |
|---|---|---|
| Data | Audio quality, labels, class balance, leakage | Data testing |
| Model | Predictions on unseen data | Model testing |
| Metrics | Accuracy, precision, recall, F1-score | Performance evaluation |
| Errors | Wrong predictions and their patterns | Error analysis |
| System | Frontend + Backend + API + Model integration | System testing |

## 3. Dataset Under Test
- **Dataset:** DementiaNet (audio clips, author-provided Colab starter code)
- **Audio folders:** `dementia/` and `nodementia/` (.wav files)
- **Label files:** `train_dm.csv`, `valid_dm.csv`
- **Metadata:** maintained in a Google Sheet by the dataset authors

## 4. Progress Status (as of 29 Oct 2026)

| # | Sprint / User story | Planned dates | Status |
|---|---|---|---|
| 1 | Testing planning | 10 Aug – 8 Sep 2026 | Completed (this document) |
| 2 | Data testing | 9 Sep – 8 Oct 2026 | Sprint window completed. Test cases D1–D8 defined; record results below |
| 3 | Model testing | 9 Oct – 7 Nov 2026 | **In progress** (current sprint) |
| 4 | Performance evaluation | 8 Nov – 7 Dec 2026 | Upcoming |
| 5 | Error analysis | 8 Dec 2026 – 6 Jan 2027 | Upcoming |
| 6 | System testing | 7 Jan – 5 Feb 2027 | Upcoming (depends on team's web integration) |
| 7 | Documentation | 6 Feb – 7 Mar 2027 | Upcoming |
| 8 | Final review | 8 Mar – 10 Mar 2027 | Upcoming |

## 5. Test Cases

### 5.1 Data testing (Sprint 2)
| ID | Test | Expected result | Status | Actual result / notes |
|---|---|---|---|---|
| D1 | Count .wav files in `dementia` and `nodementia` | Counts match CSV records | Done | _fill count_ |
| D2 | Open every audio file | No corrupt or empty files | Done | _fill result_ |
| D3 | Check sample rate and channels | Consistent (or handled in preprocessing) | Done | _fill result_ |
| D4 | Check duration | No file shorter than 1 second | Done | _fill result_ |
| D5 | Check labels in train/valid CSV | No missing or wrong labels | Done | _fill result_ |
| D6 | Check duplicates | No duplicate rows or files | Done | _fill result_ |
| D7 | Train/valid overlap | Zero overlap (no data leakage) | Done | _fill result_ |
| D8 | Class balance | Imbalance noted and handled | Done | _fill class ratio_ |

### 5.2 Model testing (Sprint 3, in progress)
| ID | Test | Expected result | Status | Actual result / notes |
|---|---|---|---|---|
| M1 | Predict on unseen test audio | Valid label and confidence for each file | In progress | |
| M2 | Very short audio | Handled without crash | Pending | |
| M3 | Noisy audio | Prediction returned, accuracy drop noted | Pending | |
| M4 | Silent audio | Graceful error or "no speech" message | Pending | |
| M5 | Same input twice | Same output (reproducible) | Pending | |

### 5.3 System testing (Sprint 6, upcoming)
| ID | Test | Expected result | Status |
|---|---|---|---|
| S1 | Upload .wav from frontend | File reaches backend | Not started |
| S2 | Wrong file type (.mp3, .txt) | Clear error message | Not started |
| S3 | API request to model | Returns prediction in valid format | Not started |
| S4 | Result shown on dashboard | Risk and prediction displayed clearly | Not started |
| S5 | Large file / slow network | No crash, timeout handled | Not started |

## 6. Evaluation Metrics
- Accuracy, Precision, Recall, F1-score
- Confusion matrix and ROC curve
- **Recall is prioritized**, because missing a real dementia case is more costly than a false alarm.

## 7. Tools
Python, pandas, scikit-learn, soundfile/librosa, matplotlib, pytest, Postman (API testing).

## 8. Deliverables
| File | Purpose | Status |
|---|---|---|
| `tests/data_check.py` | Automated data checks (D1–D8) | Update status after commit |
| `tests/test_model.py` | Model tests (M1–M5) | In progress |
| `tests/evaluate.py` | Metrics, confusion matrix, ROC | Not started |
| `results/` | Reports and plots | Not started |
| Final project documentation | Methodology and implementation | Not started |

## 9. Risks and Dependencies
- Model testing and evaluation depend on the trained model from the AI/ML sprint (Nishit Singhal).
- System testing depends on the frontend, backend and API integration (Vaibhav Kumar Jain) being ready by January 2027.
- Class imbalance (D8) may affect accuracy, so recall and F1-score are tracked along with accuracy.

## 10. Change Log
| Date | Change |
|---|---|
| 29 Oct 2026 | Added dataset details, sprint progress status, status columns, risks and deliverables tracking |
| Initial | First version of test plan (objective, scope, test cases, metrics, tools) |
