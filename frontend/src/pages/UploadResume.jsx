import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { uploadResume } from "../services/api";

function highlightSkillsInText(text, skills) {
  if (!skills || skills.length === 0) return text;

  // Build a regex that matches any of the detected skills, case-insensitively
  // Escape special regex characters in skill names (e.g. "C++", "C#")
  const escaped = skills.map((s) => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
  const pattern = new RegExp(`\\b(${escaped.join("|")})\\b`, "gi");

  const parts = text.split(pattern);

  return parts.map((part, idx) => {
    const isSkill = skills.some(
      (skill) => skill.toLowerCase() === part.toLowerCase()
    );
    return isSkill ? (
      <mark key={idx} className="bg-yellow-200 text-gray-900 rounded px-0.5">
        {part}
      </mark>
    ) : (
      <span key={idx}>{part}</span>
    );
  });
}

function UploadResume() {
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    setError("");
    setResult(null);
    setFile(e.target.files[0]);
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setError("Please select a PDF file first.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await uploadResume(file);
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Upload failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 px-4 py-10">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-2xl">
        <h2 className="text-2xl font-bold mb-6 text-center text-blue-600">
          Upload Resume
        </h2>

        <form onSubmit={handleUpload}>
          <input
            type="file"
            accept="application/pdf"
            onChange={handleFileChange}
            className="w-full mb-4 text-sm text-gray-600
                       file:mr-4 file:py-2 file:px-4
                       file:rounded file:border-0
                       file:bg-blue-50 file:text-blue-600
                       hover:file:bg-blue-100"
          />

          {error && <p className="text-red-500 text-sm mb-4">{error}</p>}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition disabled:opacity-50"
          >
            {loading ? "Uploading..." : "Upload PDF"}
          </button>
        </form>

        {result && (
          <div className="mt-6 border-t pt-4">
            <p className="text-green-600 font-semibold mb-3">
              ✅ Uploaded: {result.filename}
            </p>

            <p className="text-gray-500 text-sm mb-2">
              Detected Skills ({result.detected_skills.length}):
            </p>
            <div className="flex flex-wrap gap-2 mb-4">
              {result.detected_skills.length > 0 ? (
                result.detected_skills.map((skill, idx) => (
                  <span
                    key={idx}
                    className="bg-blue-50 text-blue-700 text-sm px-3 py-1 rounded-full"
                  >
                    {skill}
                  </span>
                ))
              ) : (
                <p className="text-gray-400 text-sm italic">
                  No known skills detected in this resume.
                </p>
              )}
            </div>

            <p className="text-gray-500 text-sm mb-1">Resume text (skills highlighted):</p>
            <div className="bg-gray-50 p-3 rounded max-h-64 overflow-y-auto text-sm text-gray-700 whitespace-pre-wrap leading-relaxed">
              {highlightSkillsInText(result.extracted_text, result.detected_skills)}
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

export default UploadResume;