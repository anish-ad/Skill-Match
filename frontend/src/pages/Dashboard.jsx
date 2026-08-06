import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getDashboard } from "../services/api";
import { useAuth } from "../context/AuthContext";

function Dashboard() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  const { user, logoutUser } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    getDashboard()
      .then((res) => setData(res.data))
      .catch(() => setError("Session expired. Please log in again."));
  }, []);

  const handleLogout = () => {
    logoutUser();
    navigate("/login");
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-sm text-center">
        <h2 className="text-2xl font-bold mb-4 text-blue-600">Dashboard</h2>

        {error && <p className="text-red-500">{error}</p>}

        {data && (
          <p className="text-gray-700 mb-6">{data.message}</p>
        )}

        <p className="text-gray-500 mb-6">Logged in as: {user?.email}</p>

        <button
          onClick={handleLogout}
          className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 transition"
        >
          Logout
        </button>
      </div>
    </div>
  );
}

export default Dashboard;