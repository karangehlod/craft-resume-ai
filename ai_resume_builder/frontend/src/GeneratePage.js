import React, { useState } from "react";

function GeneratePage() {
  const [userDetails, setUserDetails] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [generatedResume, setGeneratedResume] = useState(null);

  const handleUserDetailsChange = (e) => {
    setUserDetails(e.target.value);
  };

  const handleGenerateResume = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await fetch("http://localhost:5000/generate_resume", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_details: userDetails,
          job_skills: result ? result.missing_skills : [],
        }),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const result = await response.json();
      setGeneratedResume(result);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Generate Resume</h2>
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
    </div>
  );
}

export default GeneratePage;
