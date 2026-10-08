# Test Plan: AI-Based Tool for Early-Stage Dementia Detection

**Project ID:** SKIT/AI/2023-2027  
**Branch:** CSE (AI), Section B  
**Prepared by:** Narendra Chaudhary (Testing, Evaluation & Documentation)

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

## 3. Test Cases

### 3.1 Data testing
| ID | Test | Expected result |
|---|---|---|
| D1 | Count .wav files in `dementia` and `nodementia` | Counts match CSV records |
| D2 | Open every audio file | No corrupt or empty files |
| D3 | Check sample rate and channels | Consistent (or handled in preprocessing) |
| D4 | Check duration | No file shorter than 1 second |
| D5 | Check labels in train/valid CSV | No missing or wrong labels |
| D6 | Check duplicates | No duplicate rows or files |
| D7 | Train/valid overlap | Zero overlap (no data leakage) |
| D8 | Class balance | Imbalance noted and handled |

### 3.2 Model testing
| ID | Test | Expected result |
|---|---|---|
| M1 | Predict on unseen test audio | Valid label and confidence for each file |
| M2 | Very short audio | Handled without crash |
| M3 | Noisy audio | Prediction returned, accuracy drop noted |
| M4 | Silent audio | Graceful error or "no speech" message |
| M5 | Same input twice | Same output (reproducible) |

### 3.3 System testing
| ID | Test | Expected result |
|---|---|---|
| S1 | Upload .wav from frontend | File reaches backend |
| S2 | Wrong file type (.mp3, .txt) | Clear error message |
| S3 | API request to model | Returns prediction in valid format |
| S4 | Result shown on dashboard | Risk and prediction displayed clearly |
| S5 | Large file / slow network | No crash, timeout handled |

## 4. Evaluation Metrics
- Accuracy, Precision, Recall, F1-score
- Confusion matrix and ROC curve
- **Recall is prioritized**, because missing a real dementia case is more costly than a false alarm.

## 5. Tools
Python, pandas, scikit-learn, soundfile/librosa, matplotlib, pytest, Postman (API testing).

## 6. Deliverables
`tests/data_check.py`, `tests/test_model.py`, `tests/evaluate.py`, `results/` (reports and plots), final project documentation.
