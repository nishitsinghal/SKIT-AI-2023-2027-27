
import speech_recognition as sr
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent
AUDIO_FILE = BASE_DIR / "dataset" / "input_speech.wav"
OUTPUT_FILE = BASE_DIR / "transcript.txt"


def convert_speech_to_text(audio_path):
    """Convert a WAV audio file into text using speech recognition."""

    recognizer = sr.Recognizer()
    audio_path = Path(audio_path)

    if not audio_path.exists():
        print(f"Error: Audio file not found: {audio_path}")
        return None

    try:
        with sr.AudioFile(str(audio_path)) as source:
            print("Loading audio...")
            audio_data = recognizer.record(source)

        print("Converting speech to text...")

        # Requires an internet connection
        text = recognizer.recognize_google(
            audio_data,
            language="en-IN"
        )

        return text

    except sr.UnknownValueError:
        print("Could not understand the audio.")
    except sr.RequestError as error:
        print(f"Speech recognition service error: {error}")
    except Exception as error:
        print(f"Unexpected error: {error}")

    return None


def save_transcript(text, output_path):
    """Save the recognized speech to a text file."""

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(text + "\n", encoding="utf-8")
    print(f"Transcript saved to: {output_path}")


def main():
    print("=== Speech-to-Text Module ===")

    transcript = convert_speech_to_text(AUDIO_FILE)

    if transcript:
        print("\nRecognized Speech:")
        print(transcript)

        save_transcript(transcript, OUTPUT_FILE)
    else:
        print("Transcription was unsuccessful.")


if __name__ == "__main__":
    main()
