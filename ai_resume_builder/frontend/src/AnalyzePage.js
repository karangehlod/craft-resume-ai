import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function AnalyzePage() {
  const [jobDescription, setJobDescription] = useState("");
  const [resumeFile, setResumeFile] = useState(null);
  const [resumeText, setResumeText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleJobDescriptionChange = (e) => {
    setJobDescription(e.target.value);
  };

  const handleResumeFileChange = (e) => {
    setResumeFile(e.target.files[0]);
  };

  const handleResumeTextChange = (e) => {
    setResumeText(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    const formData = new FormData();
    formData.append("job_description", jobDescription);
    if (resumeFile) {
      formData.append("resume_file", resumeFile);
    }
    formData.append("resume_text", resumeText);

    try {
      const response = await fetch("http://localhost:5000/analyze_resume", {
        method: "POST",
        body: formData,
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const result = await response.json();
      setResult(result);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Analyze Resume</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="jobDescription">Job Description:</label>
          <textarea
            id="jobDescription"
            value={jobDescription}
            onChange={handleJobDescriptionChange}
            required
          />
        </div>
        <div>
          <label htmlFor="resumeFile">Upload Resume:</label>
          <input
            type="file"
            id="resumeFile"
            accept=".pdf,.doc,.docx"
            onChange={handleResumeFileChange}
          />
        </div>
        <div>
          <label htmlFor="resumeText">Resume Text:</label>
          <textarea
            id="resumeText"
            value={resumeText}
            onChange={handleResumeTextChange}
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? "Analyzing..." : "Analyze Resume"}
        </button>
      </form>
      {result && (
        <div className="result-box">
          <h2>Analysis Result</h2>
          <p>Missing Skills: {result.missing_skills.join(", ")}</p>
          <p>Match Percentage: {result.score}%</p>
          <p>Suggested Keywords: {result.suggested_keywords.join(", ")}</p>
        </div>
      )}
    </div>
  );
}

export default AnalyzePage;
