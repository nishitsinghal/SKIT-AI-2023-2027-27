# AI-based Tool for Early Stage Dementia Detection

**Repository:** [narendra72/SKIT-AI-2023-2027-27](https://github.com/nishitsinghal/SKIT-AI-2023-2027-27)

**Project ID:** SKIT/AI/2023-2027/27
**Branch:** CSE (AI)
**Section:** B
**Session:** 2026-27

---

## 📌 Overview

Early-stage dementia can be difficult to identify because early cognitive and communication changes are often subtle. Traditional screening relies on clinical interviews and cognitive assessments, which are manual and time-consuming.

This project builds a system that analyzes a person's speech using **NLP, speech processing, and machine learning** techniques to identify dementia-related linguistic and acoustic patterns, generating a **risk score** to support further clinical evaluation.

## 🎯 SDG Mapping

**SDG 3 — Good Health and Well-Being**

## 🏗️ Project Track

- ✅ R&D Innovation
- ✅ Mandatory External Evaluation: Research Paper Publication

## 📊 Dataset

- Built on the **DementiaNet** dataset (sourced via GitHub, no approval required)
- Includes audio clips, CSV label files (`train_dm.csv`, `valid_dm.csv`), metadata in a linked Google Sheet, and author-provided Colab starter code
- Local dataset organized into two class folders of `.wav` audio files:

```
dataset/
├── dementia/       # .wav files — dementia class
└── nodementia/     # .wav files — no-dementia class
```

- File counts per class are verified using a simple Python script that recursively globs `*.wav` files in each folder

---

## 🛠️ Technology Stack

| Tool / Technology | Layer | Type | Purpose |
|---|---|---|---|
| React.js | Frontend | Software | UI for speech recording & display of screening results |
| Node.js & Express.js | Backend | Software | REST APIs & app logic connecting frontend, AI service & database |
| Python | AI/ML | Software | Data preprocessing, feature engineering, model training |
| Scikit-learn | AI/ML | Software | Classical ML models, preprocessing & evaluation |
| TensorFlow | AI/ML | Software | Deep learning experiments for speech/text classification |
| Speech-to-Text | Speech Processing | Software | Convert recorded speech into text for NLP analysis |
| NLP Libraries | AI/NLP | Software | Extract linguistic and textual features |
| Audio Processing Libraries | Speech Processing | Software | Noise handling & extraction of acoustic features |
| MySQL | Backend | Software | Store user information and prediction records |
| REST API | Backend/AI | Software | Expose model inference & risk score results |
| Git & GitHub | Development | Software | Version control, collaboration & management |

---

## 🚀 Proposed Sprints

| # | Sprint Name | User Story |
|---|---|---|
| 1 | Requirements & Dataset | Define project requirements & identify a suitable speech/text dataset |
| 2 | Data Preparation | Clean the data & prepare speech/text features for analysis |
| 3 | Speech & NLP | Implement speech-to-text and extract acoustic/NLP features |
| 4 | ML/DL Model | Train, compare and evaluate suitable dementia risk-prediction models |
| 5 | Web Integration | Integrate the selected model with Node.js, API and frontend into the final tool |

---

## 👥 Team

| Name | Expertise Area | Role |
|---|---|---|
| Vaibhav Kumar Jain (Team Lead) | Web Development | Develop the Node.js frontend and Flask-based backend |
| Narendra Choudhary | Testing / Documentation | Perform testing, model evaluation & documentation |
| Nishit Singhal | AI/ML | Lead AI/ML model development & project integration |
| Sujal Solanki | NLP/Python | Handle NLP and speech processing tasks |

---

## 🧩 Roles & Responsibilities

### Team Lead — Vaibhav Kumar Jain
**Sprint:** Web Development and AI Integration

| User Story | Timeline | Task |
|---|---|---|
| Frontend Planning | Aug '26 | Design the UI for speech and text input |
| UI Development | Sep '26 | Develop web pages for user interaction & data input |
| Speech & Text Input | Sep–Oct '26 | Add audio recording/upload and text response functionality |
| Backend Development | Oct–Nov '26 | Develop Node.js-based backend for handling user requests |
| API Development | Dec '26–Jan '27 | Create APIs for connecting frontend with ML model |
| Model Connection | Jan–Feb '27 | Integrate the prediction model with the backend API |
| Result Dashboard | Feb–Mar '27 | Display risk score and prediction results clearly |
| Final Web Integration | Mar '27 | Complete frontend-backend integration & prepare web tool |

### Member — Narendra Choudhary
**Sprint:** Testing, Evaluation & Documentation

| User Story | Timeline | Task |
|---|---|---|
| Testing Planning | Aug–Sep '26 | Prepare test cases for the complete system |
| Data Testing | Sep '26 | Check dataset quality, labels and preprocessing results |
| Model Testing | Sep–Oct '26 | Test model predictions on unseen data |
| Performance Evaluation | Nov '26 | Evaluate accuracy, precision, recall & F1-score |
| Error Analysis | Dec '26–Jan '27 | Identify prediction errors & possible system issues |
| System Testing | Jan–Feb '27 | Test frontend, backend, API and model integration |
| Documentation | Feb–Mar '27 | Document project methodology and implementation |
| Final Review | Mar '27 | Perform final testing and prepare project documentation |

### Member — Nishit Singhal
**Sprint:** AI/ML Model Development

| User Story | Timeline | Task |
|---|---|---|
| ML Planning | Aug–Sep '26 | Identify suitable ML/DL approaches for dementia detection |
| Feature Preparation | Sep '26 | Prepare suitable features for ML model development |
| Baseline Model | Oct–Nov '26 | Develop initial ML models for dementia-risk prediction |
| Model Training | Nov–Dec '26 | Train different models using prepared features |
| Model Comparison | Dec '26–Jan '27 | Compare models using suitable evaluation metrics |
| Model Optimization | Feb '27 | Improve model performance through feature/model tuning |
| Model Evaluation | Feb–Mar '27 | Evaluate the selected model on unseen test data |
| Model Integration | Mar '27 | Integrate the final trained model with the application |

### Member — Sujal Solanki
**Sprint:** NLP and Speech Processing

| User Story | Timeline | Task |
|---|---|---|
| Speech Processing | Aug–Sep '26 | Prepare and preprocess speech data for analysis |
| Speech to Text | Sep–Oct '26 | Convert user speech into text using speech recognition |
| Text Preprocessing | Oct–Nov '26 | Clean and prepare transcripts for NLP analysis |
| NLP Feature Extraction | Nov–Dec '26 | Extract relevant linguistic features from text responses |
| Acoustic Features | Dec '26–Jan '27 | Extract useful speech/acoustic features from audio |
| NLP Model Preparation | Jan–Feb '27 | Prepare text features for dementia-risk prediction |
| Feature Integration | Feb–Mar '27 | Combine relevant NLP and speech features for modeling |
| NLP Pipeline Integration | Mar '27 | Integrate the NLP and speech processing pipeline with the ML system |

---

## 📈 Project Status

Currently in the requirements & dataset preparation phase, building on the DementiaNet dataset and author-provided starter code, with next steps focused on loading the CSVs, extending the starter pipeline, adding evaluation metrics, and building a Streamlit demo interface for evaluation.

---

## ✅ Approval

Verified & Approved By: **Kapil Sharma** (22/08/26)
