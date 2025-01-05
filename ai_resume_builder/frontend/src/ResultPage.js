import React from 'react';
import { useLocation } from 'react-router-dom';

function ResultPage() {
  const location = useLocation();
  const { result, jobDescription } = location.state || {};

  const calculateMatchPercentage = (missingSkills, jobDescription) => {
    const jobSkills = jobDescription.split(" ").length;
    const missingSkillsCount = missingSkills.length;
    const matchPercentage =
      ((jobSkills - missingSkillsCount) / jobSkills) * 100;
    return matchPercentage.toFixed(2);
  };

  if (!result) {
    return <p>No result available. Please go back and analyze a resume.</p>;
  }

  return (
    <div className="result-box">
      <h2>Analysis Result</h2>
      <p>Missing Skills: {result.missing_skills.join(", ")}</p>
      <p>
        Match Percentage:{" "}
        {calculateMatchPercentage(result.missing_skills, jobDescription)}%
      </p>
      <button onClick={() => window.history.back()}>Analyze Another Resume</button>
    </div>
  );
}

export default ResultPage;
