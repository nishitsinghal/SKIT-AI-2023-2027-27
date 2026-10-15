import { useState } from "react";
import axios from "axios";
import "./App.css";
import TextScreening from "./TextScreening";

const API = "http://localhost:5000/api/users";

function App() {
  const [mode, setMode] = useState("login");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState("");
  const [loading, setLoading] = useState(false);
  const [isDashboard, setIsDashboard] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);
  const [currentPage, setCurrentPage] = useState("dashboard");

  const handleSubmit = async (e) => {
    e.preventDefault();

    setMessage("");
    setMessageType("");

    const cleanEmail = email.trim().toLowerCase();

    if (mode === "signup" && name.trim().length < 2) {
      setMessage("Please enter your full name.");
      setMessageType("error");
      return;
    }

    if (password.length < 8) {
      setMessage("Password must contain at least 8 characters.");
      setMessageType("error");
      return;
    }

    if (mode === "signup" && password !== confirmPassword) {
      setMessage("Passwords do not match.");
      setMessageType("error");
      return;
    }

    setLoading(true);

    try {
      if (mode === "signup") {
        await axios.post(API, {
          name: name.trim(),
          email: cleanEmail,
          password,
        });

        setMode("login");
        setPassword("");
        setConfirmPassword("");
        setMessage("Account created successfully. Please sign in.");
        setMessageType("success");
      } else {
        const response = await axios.post(`${API}/login`, {
          email: cleanEmail,
          password,
        });

        if (!response.data.token) {
          throw new Error("Login response did not include a token.");
        }

        localStorage.setItem("token", response.data.token);

        setCurrentUser(response.data.user);
        setIsDashboard(true);
      }
    } catch (error) {
      setMessage(
        error.response?.data?.message ||
        (error.response
          ? "Something went wrong. Please try again."
          : "Unable to connect to the server. Please check your backend.")
      );

      setMessageType("error");
    } finally {
      setLoading(false);
    }
  };

  const switchMode = (nextMode) => {
    setMode(nextMode);
    setMessage("");
    setMessageType("");
    setPassword("");
    setConfirmPassword("");
    setShowPassword(false);
  };

  if (isDashboard && currentPage === "text-screening") {
    return (
      <TextScreening
        userName={currentUser?.name}
        onBack={() => setCurrentPage("dashboard")}
      />
    );
  }


  if (isDashboard) {
    return (
      <main className="dashboard-page">
        <header className="dashboard-header">
          <div className="brand">
            <div className="brand-icon">AI</div>
            <span>
              CognitiveCare <b>AI</b>
            </span>
          </div>

          <button
            className="logout-button"
            onClick={() => {
              localStorage.removeItem("token");
              setCurrentPage("dashboard");
              setCurrentUser(null);
              setIsDashboard(false);
              setMode("login");
              setPassword("");
              setMessage("");
            }}
          >
            Log out
          </button>
        </header>

        <section className="dashboard-content">
          <p className="eyebrow">YOUR SCREENING WORKSPACE</p>

          <h1>
            Welcome, {currentUser?.name || "User"}!
          </h1>

          <p className="dashboard-description">
            Explore the available screening options in your
            cognitive health research workspace.
          </p>

          <div className="dashboard-cards">
            <article className="dashboard-card">
              <div className="dashboard-card-icon">T</div>
              <h2>Text Screening</h2>
              <p>
                Enter text for the planned AI-based cognitive
                screening workflow.
              </p>

              <button
                className="dashboard-action"
                onClick={() => {
                  setMessage("");
                  setCurrentPage("text-screening");
                }}
              >
                Explore text screening →
              </button>

            </article>

            <article className="dashboard-card">
              <div className="dashboard-card-icon">S</div>
              <h2>Speech Screening</h2>
              <p>
                Prepare for speech-based screening using the
                planned speech analysis module.
              </p>
              <button
                className="dashboard-action"
                onClick={() =>
                  setMessage(
                    "Speech screening page is the next feature to build."
                  )
                }
              >
                Explore speech screening →
              </button>
            </article>
          </div>

          {message && (
            <p className="dashboard-notice" role="status">
              {message}
            </p>
          )}

          <p className="dashboard-disclaimer">
            This project supports preliminary screening research
            and does not provide a medical diagnosis.
          </p>
        </section>
      </main>
    );
  }


  return (
    <main className="auth-page">
      {/* Left Welcome Panel */}
      <section className="welcome-panel">
        <div className="brand">
          <div className="brand-icon">AI</div>
          <span>
            CognitiveCare <b>AI</b>
          </span>
        </div>

        <div className="welcome-content">
          <div className="brain-illustration">
            <div className="brain-circle">
              <svg viewBox="0 0 120 120" aria-hidden="true">
                <path
                  d="M59 26 C44 10 24 25 30 42 C12 49 21 70 34 73 C27 91 45 103 59 91 L59 26"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="3"
                  strokeLinecap="round"
                />

                <path
                  d="M61 26 C76 10 96 25 90 42 C108 49 99 70 86 73 C93 91 75 103 61 91 L61 26"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="3"
                  strokeLinecap="round"
                />

                <path
                  d="M34 44 L48 48 L43 62 L58 68 M86 44 L72 48 L77 62 L62 68 M40 81 L53 78 M80 81 L67 78"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2.5"
                  strokeLinecap="round"
                />
              </svg>
            </div>

            <span className="orbit orbit-one"></span>
            <span className="orbit orbit-two"></span>
          </div>

          <p className="eyebrow">
            AI-POWERED COGNITIVE SCREENING
          </p>

          <h1>
            Understand cognitive health. Take the first step.
          </h1>

          <p className="welcome-description">
            An AI-based tool exploring speech and text patterns
            to support early-stage dementia risk screening and
            cognitive health research.
          </p>
        </div>

        <div className="trust-row">
          <div>
            <span>✓</span> Speech &amp; Text Analysis
          </div>

          <div>
            <span>✓</span> Research-Focused Screening
          </div>
        </div>
      </section>

      {/* Right Authentication Panel */}
      <section className="form-panel">
        <div className="mobile-brand">
          <div className="brand-icon">AI</div>
          <span>
            CognitiveCare <b>AI</b>
          </span>
        </div>

        <div className="auth-card">
          <div className="form-heading">
            <p className="eyebrow">
              {mode === "login"
                ? "YOUR SCREENING WORKSPACE"
                : "GET STARTED"}
            </p>

            <h2>
              {mode === "login"
                ? "Welcome back"
                : "Create your account"}
            </h2>

            <p>
              {mode === "login"
                ? "Sign in to continue to your workspace."
                : "Create an account to get started."}
            </p>
          </div>

          {/* Login and Signup Tabs */}
          <div className="auth-tabs">
            <button
              type="button"
              className={mode === "login" ? "active" : ""}
              onClick={() => switchMode("login")}
              aria-pressed={mode === "login"}
            >
              Sign in
            </button>

            <button
              type="button"
              className={mode === "signup" ? "active" : ""}
              onClick={() => switchMode("signup")}
              aria-pressed={mode === "signup"}
            >
              Create account
            </button>
          </div>

          <form onSubmit={handleSubmit}>
            {/* Full Name: Signup Only */}
            {mode === "signup" && (
              <div className="field">
                <label htmlFor="name">Full name</label>

                <input
                  id="name"
                  type="text"
                  placeholder="Enter your full name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  autoComplete="name"
                  minLength={2}
                  maxLength={80}
                  required
                />
              </div>
            )}

            {/* Email */}
            <div className="field">
              <label htmlFor="email">Email address</label>

              <input
                id="email"
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                autoComplete="email"
                required
              />
            </div>

            {/* Password */}
            <div className="field">
              <label htmlFor="password">Password</label>

              <div className="password-wrap">
                <input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  placeholder="At least 8 characters"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  autoComplete={
                    mode === "login"
                      ? "current-password"
                      : "new-password"
                  }
                  minLength={8}
                  required
                />

                <button
                  className="password-toggle"
                  type="button"
                  onClick={() =>
                    setShowPassword((previous) => !previous)
                  }
                  aria-label={
                    showPassword ? "Hide password" : "Show password"
                  }
                >
                  {showPassword ? "Hide" : "Show"}
                </button>
              </div>
            </div>

            {/* Confirm Password: Signup Only */}
            {mode === "signup" && (
              <div className="field">
                <label htmlFor="confirmPassword">
                  Confirm password
                </label>

                <input
                  id="confirmPassword"
                  type={showPassword ? "text" : "password"}
                  placeholder="Enter your password again"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  autoComplete="new-password"
                  minLength={8}
                  required
                />
              </div>
            )}

            {/* Login Options */}
            {mode === "login" && (
              <div className="form-options">
                <span className="secure-note">
                  🔒 Secure sign in
                </span>

                <span className="forgot-note">
                  Forgot password?
                </span>
              </div>
            )}

            {/* Success and Error Messages */}
            {message && (
              <div
                className={`status-message ${messageType}`}
                role="status"
                aria-live="polite"
              >
                {message}
              </div>
            )}

            {/* Submit Button */}
            <button
              className="submit-button"
              type="submit"
              disabled={loading}
            >
              {loading
                ? "Please wait..."
                : mode === "login"
                  ? "Sign in to your account"
                  : "Create my account"}

              {!loading && <span>→</span>}
            </button>
          </form>

          {/* Switch Authentication Mode */}
          <p className="switch-prompt">
            {mode === "login"
              ? "New to CognitiveCare AI?"
              : "Already have an account?"}

            <button
              type="button"
              onClick={() =>
                switchMode(mode === "login" ? "signup" : "login")
              }
            >
              {mode === "login"
                ? " Create an account"
                : " Sign in"}
            </button>
          </p>

          {/* Medical Disclaimer */}
          <div className="disclaimer">
            <span>ⓘ</span>
            This tool supports screening research and is not a
            medical diagnosis.
          </div>
        </div>

        <p className="copyright">
          CognitiveCare AI · Cognitive health research
        </p>
      </section>
    </main>
  );
}

export default App;