const { useState } = React;

function App() {
  const [jobDescription, setJobDescription] = useState("");
  const [resumeText, setResumeText] = useState("");
  const [resumeFile, setResumeFile] = useState(null);
  const [output, setOutput] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = (e) => {
    e.preventDefault();
    // Handle login logic here
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("job_description", jobDescription);
    formData.append("resume_text", resumeText);
    if (resumeFile) {
      formData.append("resume_file", resumeFile);
    }

    const response = await fetch("/analyze_resume", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const data = await response.json();
      setOutput(`Missing Skills: ${data.missing_skills.join(", ")}\nScore: ${data.score}%\nSuggested Keywords: ${data.suggested_keywords.join(", ")}`);
    } else {
      setOutput("Error analyzing resume.");
    }
  };

  return (
    <div>
      <h1>AI-Driven Resume Builder</h1>
      <p>Welcome to the AI-Driven Resume Builder. Please log in or continue as a guest.</p>
      <form onSubmit={handleLogin}>
        <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username" />
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" />
        <button type="submit">Login</button>
      </form>
      <form onSubmit={handleSubmit}>
        <textarea value={jobDescription} onChange={(e) => setJobDescription(e.target.value)} placeholder="Paste job description here"></textarea>
        <textarea value={resumeText} onChange={(e) => setResumeText(e.target.value)} placeholder="Paste your resume here"></textarea>
        <input type="file" onChange={(e) => setResumeFile(e.target.files[0])} />
        <button type="submit">Analyze Resume</button>
      </form>
      <div id="output">{output}</div>
    </div>
  );
}

ReactDOM.render(<App />, document.getElementById('root'));
