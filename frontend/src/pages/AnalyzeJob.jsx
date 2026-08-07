import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { analyzeJob } from "../services/api";

function AnalyzeJob() {
  const [formData, setFormData] = useState({ title: "", description: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setResult(null);
    setLoading(true);

    try {
      const response = await analyzeJob(formData);
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Analysis failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 px-4 py-10">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-lg">
        <h2 className="text-2xl font-bold mb-6 text-center text-blue-600">
          Analyze Job Description
        </h2>

        <form onSubmit={handleSubmit}>
          <input
            type="text"
            name="title"
            placeholder="Job Title (e.g. Backend Developer)"
            value={formData.title}
            onChange={handleChange}
            required
            className="w-full mb-4 px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />

          <textarea
            name="description"
            placeholder="Paste the full job description here..."
            value={formData.description}
            onChange={handleChange}
            required
            rows={8}
            className="w-full mb-4 px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          />

          {error && <p className="text-red-500 text-sm mb-4">{error}</p>}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition disabled:opacity-50"
          >
            {loading ? "Analyzing..." : "Extract Skills"}
          </button>
        </form>

        {result && (
          <div className="mt-6 border-t pt-4">
            <p className="text-green-600 font-semibold mb-3">
              ✅ Analyzed: {result.title}
            </p>
            <p className="text-gray-500 text-sm mb-2">
              Extracted Skills ({result.extracted_skills.length}):
            </p>
            <div className="flex flex-wrap gap-2">
              {result.extracted_skills.map((skill, idx) => (
                <span
                  key={idx}
                  className="bg-blue-50 text-blue-700 text-sm px-3 py-1 rounded-full"
                >
                  {skill}
                </span>
              ))}
            </div>
          </div>
        )}

        <button
          onClick={() => navigate("/dashboard")}
          className="w-full mt-6 text-blue-600 text-sm hover:underline"
        >
          Back to Dashboard
        </button>
      </div>
    </div>
  );
}

export default AnalyzeJob;