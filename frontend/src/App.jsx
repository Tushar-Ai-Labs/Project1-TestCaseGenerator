import { useState } from 'react'
import './App.css'

function App() {
  const [feature, setFeature] = useState('')
  const [testType, setTestType] = useState('all') // 'all', 'positive', 'negative'
  const [testCases, setTestCases] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleGenerate = async () => {
    if (!feature.trim()) return;

    setLoading(true);
    setError(null);
    setTestCases(null);

    try {
      const response = await fetch('http://localhost:5000/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          feature_description: feature,
          test_type: testType
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || `Error: ${response.statusText}`);
      }

      if (data.error) {
        throw new Error(data.error);
      }
      setTestCases(data.test_cases);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  const handleExport = () => {
    if (!testCases) return;
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify({ test_cases: testCases }, null, 2));
    const downloadAnchorNode = document.createElement('a');
    downloadAnchorNode.setAttribute("href", dataStr);
    downloadAnchorNode.setAttribute("download", "test_cases.json");
    document.body.appendChild(downloadAnchorNode); // required for firefox
    downloadAnchorNode.click();
    downloadAnchorNode.remove();
  }

  return (
    <div className="container">
      <header>
        <div className="logo-container">
          <span className="logo-icon">🤖</span>
          <span className="logo-text">Autopilot QA</span>
        </div>
        <h1>Test Case Generator</h1>
        <p>AI-Powered Automation Suite</p>
      </header>

      <main>
        <section className="input-section">
          <textarea
            value={feature}
            onChange={(e) => setFeature(e.target.value)}
            placeholder="Describe the feature or user story here (e.g., 'Login page with email validation')..."
            rows={5}
          />

          <div className="controls">
            <label>Test Type:</label>
            <select value={testType} onChange={(e) => setTestType(e.target.value)}>
              <option value="all">All Test Cases</option>
              <option value="positive">Positive Only (Happy Paths)</option>
              <option value="negative">Negative Only (Edge Cases)</option>
            </select>
          </div>

          <button
            onClick={handleGenerate}
            disabled={loading || !feature.trim()}
            className="generate-btn"
          >
            {loading ? (
              <>
                <span className="spinner"></span> Generating...
              </>
            ) : 'Generate Test Cases'}
          </button>
        </section>

        {error && <div className="error-message">{error}</div>}

        {testCases && (
          <section className="results-section">
            <div className="results-header">
              <h2>Generated Test Cases</h2>
              <button onClick={handleExport} className="export-btn">Download JSON</button>
            </div>

            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Title</th>
                    <th>Preconditions</th>
                    <th>Steps</th>
                    <th>Expected Result</th>
                  </tr>
                </thead>
                <tbody>
                  {testCases.map((tc, index) => (
                    <tr key={index}>
                      <td>{tc.id || `TC_${index + 1}`}</td>
                      <td>{tc.title}</td>
                      <td>{tc.preconditions}</td>
                      <td>
                        <ol>
                          {Array.isArray(tc.steps) ? tc.steps.map((step, i) => <li key={i}>{step}</li>) : <li>{tc.steps}</li>}
                        </ol>
                      </td>
                      <td>{tc.expected_result}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        )}
      </main>
    </div>
  )
}

export default App
