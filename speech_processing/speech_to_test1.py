
import speech_recognition as sr
from pathlib import Path

def speech_to_text(audio_file):
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(str(audio_file)) as source:
            print("Reading audio file...")
            audio = recognizer.record(source)

        print("Converting speech to text...")
        text = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        print("\nTranscribed Text:")
        print(text)

        # Save transcript
        output_file = Path("transcript.txt")
        output_file.write_text(text, encoding="utf-8")

        print("\nTranscript saved successfully!")
        return text

    except sr.UnknownValueError:
        print("Sorry, speech could not be understood.")
    except sr.RequestError as error:
        print(f"Recognition service error: {error}")
    except FileNotFoundError:
        print("Audio file not found.")
    except Exception as error:
        print(f"Error: {error}")

    return None


if __name__ == "__main__":
    audio_path = input(
        "Enter the path of your WAV audio file: "
    )
    speech_to_text(audio_path)
