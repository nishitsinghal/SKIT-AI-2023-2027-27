import axios from "axios";
import { useState } from "react";
import "./App.css";

const API = "http://localhost:5000/api/screening";

function TextScreening({ onBack, userName }) {
    const [responseText, setResponseText] = useState("");
    const [message, setMessage] = useState("");
    const [messageType, setMessageType] = useState("");
    const [loading, setLoading] = useState(false);

    async function handleSubmit(event) {
        event.preventDefault();

        if (!responseText.trim()) {
            setMessage("Please enter some text before submitting.");
            setMessageType("error");
            return;
        }

        setLoading(true);
        setMessage("");
        setMessageType("");

        try {
            const token = localStorage.getItem("token");

            if (!token) {
                setMessage("Your session has expired. Please log in again.");
                setMessageType("error");
                return;
            }

            const response = await axios.post(
                API,
                {
                    text: responseText.trim(),
                },
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );

            setMessage(response.data.message);
            setMessageType("success");
        } catch (error) {
            setMessage(
                error.response?.data?.message ||
                "Unable to connect to the backend. Please check that your server is running."
            );
            setMessageType("error");
        } finally {
            setLoading(false);
        }
    }

    return (
        <main className="screening-page">
            <header className="screening-header">
                <div className="brand">
                    <div className="brand-icon">AI</div>
                    <span>
                        CognitiveCare <b>AI</b>
                    </span>
                </div>

                <button
                    type="button"
                    className="logout-button"
                    onClick={onBack}
                >
                    ← Dashboard
                </button>
            </header>

            <section className="screening-content">
                <p className="eyebrow">TEXT-BASED SCREENING</p>

                <h1>Text Screening</h1>

                <p className="dashboard-description">
                    Welcome, {userName || "User"}. Enter a text response
                    for your research screening workflow.
                </p>

                <form
                    className="screening-form"
                    onSubmit={handleSubmit}
                >
                    <label htmlFor="screening-text">
                        Your text response
                    </label>

                    <textarea
                        id="screening-text"
                        value={responseText}
                        onChange={(event) => {
                            setResponseText(event.target.value);
                            setMessage("");
                            setMessageType("");
                        }}
                        placeholder="Enter your text here..."
                        rows={8}
                        required
                    />

                    <p className="screening-helper">
                        You can enter a sample response for testing.
                        Avoid including personally identifying information.
                    </p>

                    <button
                        type="submit"
                        className="dashboard-action"
                        disabled={!responseText.trim() || loading}
                    >
                        {loading ? "Submitting..." : "Submit Response"}
                    </button>
                </form>

                {message && (
                    <p
                        className={`screening-message ${messageType}`}
                        role="status"
                    >
                        {message}
                    </p>
                )}

                <p className="dashboard-disclaimer">
                    This research prototype does not diagnose dementia.
                    The current backend receives text but does not yet
                    save it to MongoDB or perform AI analysis.
                </p>
            </section>
        </main>
    );
}

export default TextScreening;
