from pathlib import Path
import librosa
import numpy as np
import pandas as pd

DATASET_PATH = Path("../dataset")

print("Dementia Speech Dataset - Week 2")
print("--------------------------------")

# Find all WAV files
audio_files = list(DATASET_PATH.rglob("*.wav"))

print("Total audio files:", len(audio_files))

features = []

for file in audio_files:
    try:
        # Load audio
        audio, sample_rate = librosa.load(file, sr=None)

        # Basic audio features
        duration = len(audio) / sample_rate

        # MFCC features
        mfcc = librosa.feature.mfcc(
            y=audio,
            sr=sample_rate,
            n_mfcc=13
        )

        # Mean MFCC values
        mfcc_mean = np.mean(mfcc, axis=1)

        # Standard deviation of MFCC
        mfcc_std = np.std(mfcc, axis=1)

        # Zero Crossing Rate
        zcr = np.mean(
            librosa.feature.zero_crossing_rate(audio)
        )

        # RMS Energy
        rms = np.mean(
            librosa.feature.rms(y=audio)
        )

        # Store features
        row = {
            "filename": file.name,
            "sample_rate": sample_rate,
            "duration": duration,
            "zcr": zcr,
            "rms": rms
        }

        # Add MFCC features
        for i in range(13):
            row[f"mfcc_mean_{i+1}"] = mfcc_mean[i]
            row[f"mfcc_std_{i+1}"] = mfcc_std[i]

        features.append(row)

    except Exception as e:
        print("Error processing:", file.name)
        print(e)

# Create DataFrame
df = pd.DataFrame(features)

print("\nFeature Extraction Completed")
print("----------------------------")
print("Number of samples:", len(df))
print("Number of features:", len(df.columns))

print("\nExtracted Features:")
print(df.head())

# Save features
output_file = DATASET_PATH / "audio_features.csv"
df.to_csv(output_file, index=False)

print("\nFeatures saved to:", output_file)