import { useState } from "react";
import axios from "axios";

const API_URL = "http://localhost:8000";

const AGENTS = [
  "Orchestrator",
  "Planner",
  "Researcher",
  "Coder",
  "Analyst",
  "Critic",
  "Optimizer",
  "Validator",
  "Reporter"
];

function App() {
  const [task, setTask] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const getAgentStatus = (agentName) => {
    if (!result) return "waiting";
    const confidence = result.confidence || {};
    const status = confidence[agentName] || "";
    if (status.startsWith("Confident")) return "success";
    if (status.startsWith("Low")) return "low";
    if (status.startsWith("Skipped")) return "skipped";
    return "waiting";
  };

  const getAgentIcon = (agentName) => {
    const status = getAgentStatus(agentName);
    if (status === "success") return "✅";
    if (status === "low") return "⚠️";
    if (status === "skipped") return "⏭️";
    if (loading) return "⏳";
    return "⏳";
  };

  const handleRun = async () => {
    if (!task.trim()) return;
    setLoading(true);
    setResult(null);
    setError(null);

    try {
      const response = await axios.post(`${API_URL}/run-task`, { task });
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Something went wrong!");
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadZip = () => {
    if (!result) return;
    window.open(`${API_URL}/download-zip/${result.project_folder}`, "_blank");
  };

  const handleDownloadFile = (filename) => {
    if (!result) return;
    window.open(`${API_URL}/download/${result.project_folder}/${filename}`, "_blank");
  };

  return (
    <div className="min-h-screen bg-gray-950 text-white">

      {/* header */}
      <div className="bg-gradient-to-r from-purple-600 via-pink-500 to-orange-400 p-8 text-center shadow-lg">
        <h1 className="text-5xl font-extrabold tracking-tight mb-2">
          NEXUS AI
        </h1>
        <p className="text-lg font-medium opacity-90">
          Autonomous Multi-Agent System
        </p>
      </div>

      <div className="max-w-4xl mx-auto p-6 space-y-6">

        {/* task input */}
        <div className="bg-gray-900 rounded-2xl p-6 shadow-xl border border-gray-800">
          <h2 className="text-xl font-bold mb-4 text-purple-400">
            Enter Your Task
          </h2>
          <textarea
            className="w-full bg-gray-800 text-white rounded-xl p-4 text-base border border-gray-700 focus:outline-none focus:border-purple-500 resize-none"
            rows={3}
            placeholder="e.g. Build a REST API for a todo app..."
            value={task}
            onChange={(e) => setTask(e.target.value)}
          />
          <button
            onClick={handleRun}
            disabled={loading || !task.trim()}
            className="mt-4 w-full py-3 rounded-xl font-bold text-lg bg-gradient-to-r from-purple-600 via-pink-500 to-orange-400 hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            {loading ? "Running NEXUS AI..." : "Run NEXUS AI"}
          </button>
          {error && (
            <p className="mt-3 text-red-400 text-sm">{error}</p>
          )}
        </div>

        {/* agent pipeline */}
        <div className="bg-gray-900 rounded-2xl p-6 shadow-xl border border-gray-800">
          <h2 className="text-xl font-bold mb-4 text-pink-400">
            Agent Pipeline
          </h2>
          <div className="space-y-3">
            {AGENTS.map((agent) => {
              const status = getAgentStatus(agent);
              const icon = getAgentIcon(agent);
              const confidence = result?.confidence?.[agent] || "Waiting...";
              return (
                <div
                  key={agent}
                  className={`flex items-center gap-4 p-3 rounded-xl border transition-all
                    ${status === "success" ? "border-green-500 bg-green-950" : ""}
                    ${status === "low" ? "border-yellow-500 bg-yellow-950" : ""}
                    ${status === "skipped" ? "border-gray-600 bg-gray-800" : ""}
                    ${status === "waiting" ? "border-gray-700 bg-gray-800" : ""}
                  `}
                >
                  <span className="text-2xl">{icon}</span>
                  <div className="flex-1">
                    <p className="font-bold text-white">{agent}</p>
                    <p className="text-sm text-gray-400">{confidence}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* results */}
        {result && (
          <>
            {/* summary */}
            <div className="bg-gray-900 rounded-2xl p-6 shadow-xl border border-gray-800">
              <h2 className="text-xl font-bold mb-4 text-orange-400">
                Task Summary
              </h2>
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-gray-800 rounded-xl p-4">
                  <p className="text-gray-400 text-sm">Language</p>
                  <p className="text-white font-bold text-lg">{result.language}</p>
                </div>
                <div className="bg-gray-800 rounded-xl p-4">
                  <p className="text-gray-400 text-sm">Project Folder</p>
                  <p className="text-white font-bold text-lg">{result.project_folder}</p>
                </div>
                <div className="bg-gray-800 rounded-xl p-4">
                  <p className="text-gray-400 text-sm">Files Generated</p>
                  <p className="text-white font-bold text-lg">{result.files_generated?.length || 0}</p>
                </div>
                <div className="bg-gray-800 rounded-xl p-4">
                  <p className="text-gray-400 text-sm">Tokens Used</p>
                  <p className="text-white font-bold text-lg">{result.tokens_used?.toLocaleString()}</p>
                </div>
              </div>
            </div>

            {/* output files */}
            <div className="bg-gray-900 rounded-2xl p-6 shadow-xl border border-gray-800">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-bold text-green-400">
                  Output Files
                </h2>
                <button
                  onClick={handleDownloadZip}
                  className="px-4 py-2 rounded-xl bg-gradient-to-r from-green-500 to-teal-500 font-bold text-sm hover:opacity-90 transition-all"
                >
                  Download All ZIP
                </button>
              </div>
              <div className="space-y-2">
                {result.files_generated?.map((filename) => (
                  <div
                    key={filename}
                    className="flex items-center justify-between bg-gray-800 rounded-xl p-3 border border-gray-700"
                  >
                    <div className="flex items-center gap-3">
                      <span>📄</span>
                      <span className="font-mono text-sm text-white">{filename}</span>
                    </div>
                    <button
                      onClick={() => handleDownloadFile(filename)}
                      className="px-3 py-1 rounded-lg bg-purple-600 hover:bg-purple-500 text-sm font-bold transition-all"
                    >
                      Download
                    </button>
                  </div>
                ))}
              </div>
            </div>
          </>
        )}

      </div>
    </div>
  );
}

export default App;