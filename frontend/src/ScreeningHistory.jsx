
import { useEffect, useState } from "react";
import axios from "axios";

const API = "http://localhost:5000/api/screening";

function ScreeningHistory({ onBack }) {
  const [screenings, setScreenings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const token = localStorage.getItem("token");

        if (!token) {
          setError("Please log in to view your screening history.");
          return;
        }

        const response = await axios.get(API, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        setScreenings(response.data.screenings || []);
      } catch (err) {
        setError(
          err.response?.data?.message ||
            "Unable to load screening history."
        );
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, []);

  return (
    <main className="dashboard-page">
      <section className="dashboard-content">
        <button className="dashboard-action" onClick={onBack}>
          ← Back to Dashboard
        </button>

        <h1>Screening History</h1>
        <p className="dashboard-description">
          View your previously submitted text responses.
        </p>

        {loading && <p>Loading screening history...</p>}

        {error && <p role="alert">{error}</p>}

        {!loading && !error && screenings.length === 0 && (
          <p>No screening records found.</p>
        )}

        {!loading &&
          !error &&
          screenings.map((item) => (
            <article className="dashboard-card" key={item._id}>
              <h2>Text Screening</h2>
              <p>{item.text}</p>
              <p>
                <strong>Status:</strong> {item.status}
              </p>
              <p>
                <strong>Submitted:</strong>{" "}
                {item.createdAt
                  ? new Date(item.createdAt).toLocaleString()
                  : "Date unavailable"}
              </p>
            </article>
          ))}
      </section>
    </main>
  );
}

export default ScreeningHistory;
