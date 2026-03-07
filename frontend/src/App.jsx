import { useState } from "react"
import { analyzeCode } from "./services/api"
import CallGraph from "./components/CallGraph"

export default function App() {

  const [code, setCode] = useState("")
  const [language, setLanguage] = useState("python")
  const [result, setResult] = useState(null)

  const handleAnalyze = async () => {
    const res = await analyzeCode(code, language)
    console.log(res)
    setResult(res)
  }

  return (
    <div className="bg-black text-white min-h-screen p-10">

      <h1 className="text-3xl mb-6">CodeScope 🚀</h1>

      <select
        value={language}
        onChange={(e) => setLanguage(e.target.value)}
        className="mb-4 text-black p-2"
      >
        <option value="python">Python</option>
        <option value="cpp">C++</option>
        <option value="java">Java</option>
        <option value="javascript">JavaScript</option>
      </select>

      <textarea
        className="w-full h-40 text-black p-2"
        value={code}
        onChange={(e) => setCode(e.target.value)}
        placeholder="Paste code here..."
      />

      <button
        onClick={handleAnalyze}
        className="mt-4 bg-blue-500 px-4 py-2 rounded"
      >
        Analyze Code
      </button>

      {result && (
        <div className="mt-6 bg-gray-800 p-4 rounded">

          <p>Loop Depth: {result.loop_depth}</p>

          <p>
            Functions: {result.functions?.join(", ")}
          </p>

          <p>
            Recursive Functions: {result.recursive_functions?.length > 0
              ? result.recursive_functions.join(", ")
              : "None"}
          </p>

          <p>Detected Patterns:</p>

          <ul>
            {result.patterns?.map((p, i) => (
              <li key={i}>{p}</li>
            ))}
          </ul>

          <h3>Performance Warnings</h3>

          <ul>
            {result.heatmap?.map((h, i) => (
              <li key={i}>
                Line {h.line} → {h.message}
              </li>
            ))}
          </ul>

          <p>Complexity: {result.estimated_complexity}</p>

          <CallGraph data={result.flow_data} />

        </div>
      )}

    </div>
  )
}