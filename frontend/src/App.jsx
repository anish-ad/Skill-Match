import { useState, useEffect } from "react";
import api from "./services/api";

function App() {
  const [healthData, setHealthData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    api
      .get("/health")
      .then((response) => {
        setHealthData(response.data);
      })
      .catch((err) => {
        setError(err.message);
      });
  }, []);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50">
      <h1 className="text-3xl font-bold text-blue-600 mb-4">SkillMatch</h1>

      {error && (
        <p className="text-red-500">Error connecting to backend: {error}</p>
      )}

      {healthData ? (
        <div className="bg-white shadow-md rounded-lg p-4 text-center">
          <p className="text-green-600 font-semibold">
            Status: {healthData.status}
          </p>
          <p className="text-gray-700">{healthData.message}</p>
          <p className="text-gray-700">
            Database: {healthData.database}
          </p>
        </div>
      ) : (
        !error && <p className="text-gray-500">Connecting to backend...</p>
      )}
    </div>
  );
}

export default App;