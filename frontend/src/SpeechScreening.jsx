
import { useState } from "react";
import "./App.css";

function SpeechScreening({ userName, onBack }) {
  const [audio, setAudio] = useState(null);
  const [message, setMessage] = useState("");
  const [recording, setRecording] = useState(false);

  const handleAudioChange = (event) => {
    const file = event.target.files[0];

    if (!file) return;

    if (!file.type.startsWith("audio/")) {
      setMessage("Please select a valid audio file.");
      setAudio(null);
      return;
    }

    setAudio(file);
    setMessage("");
  };

  return (
    <main className="dashboard-page">
      <section className="dashboard-content">
        <button className="dashboard-action" onClick={onBack}>
          ← Back to Dashboard
        </button>

        <h1>Speech Screening</h1>
        <p className="dashboard-description">
          Welcome, {userName || "User"}. Record or upload an audio
          response for your research screening workflow.
        </p>

        <article className="dashboard-card">
          <h2>Upload Audio</h2>
          <p>Select an audio file from your device.</p>

          <input
            type="file"
            accept="audio/*"
            onChange={handleAudioChange}
          />

          {audio && (
            <div>
              <p>Selected file: {audio.name}</p>
              <audio controls src={URL.createObjectURL(audio)} />
            </div>
          )}

          {message && <p role="alert">{message}</p>}
        </article>

        <article className="dashboard-card">
          <h2>Record Audio</h2>
          <p>
            Microphone recording will be added in the next step.
          </p>

          <button
            className="dashboard-action"
            onClick={() => setRecording(!recording)}
          >
            {recording ? "Stop" : "Recording option"}
          </button>

          {recording && (
            <p>Live recording is not implemented yet.</p>
          )}
        </article>
      </section>
    </main>
  );
}

export default SpeechScreening;
