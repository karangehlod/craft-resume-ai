import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate
import "./App.css";

function App() {
  const [jobDescription, setJobDescription] = useState("");
  const [resumeFile, setResumeFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [userDetails, setUserDetails] = useState("");
  const [generatedResume, setGeneratedResume] = useState(null);
  const navigate = useNavigate(); // Initialize useNavigate

  const handleJobDescriptionChange = (e) => {
    setJobDescription(e.target.value);
  };

  const handleResumeFileChange = (e) => {
    setResumeFile(e.target.files[0]);
  };

  const handleUserDetailsChange = (e) => {
    setUserDetails(e.target.value);
  };

  const calculateMatchPercentage = (missingSkills, jobDescription) => {
    const jobSkills = jobDescription.split(" ").length;
    const missingSkillsCount = missingSkills.length;
    const matchPercentage =
      ((jobSkills - missingSkillsCount) / jobSkills) * 100;
    return matchPercentage.toFixed(2);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    console.log("Form submitted");
    const formData = new FormData();
    formData.append("job_description", jobDescription);
    if (resumeFile) {
      formData.append("resume_file", resumeFile);
    }

    try {
      const response = await fetch("http://localhost:5000/analyze_resume", { // Ensure the correct URL
        method: "POST",
        body: formData,
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const result = await response.json();
      console.log("Response from backend:", result);
      setResult(result);
      navigate("/result", { state: { result, jobDescription } }); // Redirect to the result page with state
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateResume = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await fetch("http://localhost:5000/generate_resume", { // Ensure the correct URL
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_details: userDetails,
          job_skills: result.missing_skills,
        }),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const result = await response.json();
      console.log("Generated Resume:", result);
      setGeneratedResume(result);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1 className="App-title">Craft Resume AI</h1>
        <p>Welcome to the Craft Resume AI project!</p>
        <button onClick={() => navigate("/analyze")}>Analyze Resume</button>
        <button onClick={() => navigate("/generate")}>Generate Resume</button>
      </header>
      <main>
        {!result ? (
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
                required
              />
            </div>
            <button type="submit" disabled={loading}>
              {loading ? "Analyzing..." : "Analyze Resume"}
            </button>
          </form>
        ) : (
          <div className="result-box">
            <h2>Analysis Result</h2>
            <p>Missing Skills: {result.missing_skills.join(", ")}</p>
            <p>
              Match Percentage:{" "}
              {calculateMatchPercentage(result.missing_skills, jobDescription)}%
            </p>
            <form onSubmit={handleGenerateResume}>
              <div>
                <label htmlFor="userDetails">User Details:</label>
                <textarea
                  id="userDetails"
                  value={userDetails}
                  onChange={handleUserDetailsChange}
                  required
                />
              </div>
              <button type="submit" disabled={loading}>
                {loading ? "Generating..." : "Generate Resume"}
              </button>
            </form>
            {generatedResume && (
              <div>
                <h2>Generated Resume</h2>
                <pre>{JSON.stringify(generatedResume, null, 2)}</pre>
              </div>
            )}
            <button onClick={() => setResult(null)}>
              Analyze Another Resume
            </button>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
