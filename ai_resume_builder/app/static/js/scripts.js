document.getElementById('resumeForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const jobDescription = document.querySelector('textarea[name="jobDescription"]').value;
    const resumeText = document.querySelector('textarea[name="resumeText"]').value;

    const response = await fetch('/analyze-resume', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ job_description: jobDescription, resume_text: resumeText })
    });

    const data = await response.json();
    document.getElementById('output').innerText = data.analysis_result;
});