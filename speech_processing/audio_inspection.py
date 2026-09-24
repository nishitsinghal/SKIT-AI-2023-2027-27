from pathlib import Path
import librosa

DATASET_PATH = Path("../dataset")

audio_files = list(DATASET_PATH.rglob("*.wav"))

print("Speech Dataset Inspection")
print("-------------------------")
print("Total audio files:", len(audio_files))

if audio_files:
    sample_file = audio_files[0]
    audio, sample_rate = librosa.load(sample_file, sr=None)

    print("Sample file:", sample_file.name)
    print("Sample rate:", sample_rate, "Hz")
    print("Duration:", round(len(audio) / sample_rate, 2), "seconds")
    print("Audio channels: Mono")