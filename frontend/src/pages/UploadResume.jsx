import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { uploadResume } from "../services/api";

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
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 px-4">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
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
            <p className="text-green-600 font-semibold mb-2">
              ✅ Uploaded: {result.filename}
            </p>
            <p className="text-gray-500 text-sm mb-1">Extracted text preview:</p>
            <div className="bg-gray-50 p-3 rounded max-h-40 overflow-y-auto text-sm text-gray-700 whitespace-pre-wrap">
              {result.extracted_text.slice(0, 500)}
              {result.extracted_text.length > 500 && "..."}
            </div>
          </div>
        )}

        <button
          onClick={() => navigate("/dashboard")}
          className="w-full mt-4 text-blue-600 text-sm hover:underline"
        >
          Back to Dashboard
        </button>
      </div>
    </div>
  );
}

export default UploadResume;