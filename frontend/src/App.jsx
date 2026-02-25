import { useState, useEffect } from "react";

// ─── Config ────────────────────────────────────────────────────────────────
const API = "http://localhost:8000/api";
const TOKEN = "a0ecf2cd5ab01b28324a320414dae170b5c81bb8"; // demo user token

const headers = {
  "Content-Type": "application/json",
  Authorization: `Token ${TOKEN}`,
};

// ─── App ───────────────────────────────────────────────────────────────────
export default function App() {
  const [page, setPage] = useState("browse"); // "browse" | "dashboard"

  return (
    <div className="app">
      {/* ── Navbar ─────────────────────────────────────────────────────── */}
      <nav className="navbar">
        <h1 className="logo">🎮 Corner Console</h1>
        <div className="nav-links">
          <button
            className={page === "browse" ? "active" : ""}
            onClick={() => setPage("browse")}
          >
            Browse Consoles
          </button>
          <button
            className={page === "dashboard" ? "active" : ""}
            onClick={() => setPage("dashboard")}
          >
            My Dashboard
          </button>
        </div>
      </nav>

      {/* ── Page content ───────────────────────────────────────────────── */}
      <main className="content">
        {page === "browse" ? <BrowseConsoles /> : <Dashboard />}
      </main>
    </div>
  );
}

// ─── Browse Consoles ───────────────────────────────────────────────────────
function BrowseConsoles() {
  const [consoles, setConsoles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [bookingId, setBookingId] = useState(null); // track which card is animating

  useEffect(() => {
    fetch(`${API}/consoles/`)
      .then((r) => r.json())
      .then(setConsoles)
      .finally(() => setLoading(false));
  }, []);

  const bookConsole = async (consoleId) => {
    // Hardcoded dates for instant demo — 3-day rental starting today
    const today = new Date();
    const end = new Date(today);
    end.setDate(end.getDate() + 3);

    const body = {
      console: consoleId,
      start_date: today.toISOString().split("T")[0],
      end_date: end.toISOString().split("T")[0],
    };

    const res = await fetch(`${API}/rentals/`, {
      method: "POST",
      headers,
      body: JSON.stringify(body),
    });

    if (res.ok) {
      setBookingId(consoleId);
      setTimeout(() => setBookingId(null), 1500);
    } else {
      alert("Booking failed — check the console / server logs.");
    }
  };

  if (loading) return <p className="loading">Loading consoles…</p>;

  return (
    <>
      <h2>Available Consoles</h2>
      <div className="grid">
        {consoles.map((c) => (
          <div key={c.id} className="card">
            <img
              src={c.image_url || "https://via.placeholder.com/400x250?text=No+Image"}
              alt={c.name}
            />
            <div className="card-body">
              <h3>{c.name}</h3>
              <p className="desc">{c.description}</p>
              <div className="card-footer">
                <span className="price">₹{c.daily_price}/day</span>
                <span className="stock">
                  {c.stock_quantity} in stock
                </span>
              </div>
              <button
                className="btn btn-book"
                onClick={() => bookConsole(c.id)}
              >
                {bookingId === c.id ? "✓ Booked!" : "Book Now"}
              </button>
            </div>
          </div>
        ))}
      </div>
    </>
  );
}

// ─── Dashboard ─────────────────────────────────────────────────────────────
function Dashboard() {
  const [rentals, setRentals] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchRentals = () => {
    setLoading(true);
    fetch(`${API}/rentals/`, { headers })
      .then((r) => r.json())
      .then(setRentals)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchRentals();
  }, []);

  const mockPay = async (rentalId) => {
    const res = await fetch(`${API}/rentals/${rentalId}/mock-pay/`, {
      method: "POST",
      headers,
    });
    if (res.ok) {
      fetchRentals(); // refresh the list
    } else {
      alert("Payment failed — check server logs.");
    }
  };

  if (loading) return <p className="loading">Loading your rentals…</p>;

  if (rentals.length === 0) {
    return (
      <>
        <h2>My Rentals</h2>
        <p className="empty">You haven't booked anything yet. Go browse some consoles! 🎮</p>
      </>
    );
  }

  return (
    <>
      <h2>My Rentals</h2>
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Console</th>
              <th>Start</th>
              <th>End</th>
              <th>Total</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {rentals.map((r) => (
              <tr key={r.id}>
                <td>{r.console_name}</td>
                <td>{r.start_date}</td>
                <td>{r.end_date}</td>
                <td>₹{r.total_price}</td>
                <td>
                  <span className={`badge badge-${r.status.toLowerCase()}`}>
                    {r.status}
                  </span>
                </td>
                <td>
                  {r.status === "Pending" ? (
                    <button
                      className="btn btn-pay"
                      onClick={() => mockPay(r.id)}
                    >
                      💳 Pay Now
                    </button>
                  ) : (
                    <span className="done">—</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
