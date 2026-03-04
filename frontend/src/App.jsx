import { useState } from "react"
import { analyzeCode } from "./services/api"
import CallGraph from "./components/CallGraph";

export default function App() {

  const [code, setCode] = useState("")
  const [result, setResult] = useState(null)

  const handleAnalyze = async () => {
    const res = await analyzeCode(code)
    setResult(res)
  }

  return (
    <div className="bg-black text-white min-h-screen p-10">

      <h1 className="text-3xl mb-6">CodeScope 🚀</h1>

      <textarea
        className="w-full h-40 text-black p-2"
        value={code}
        onChange={(e) => setCode(e.target.value)}
        placeholder="Paste Python code here..."
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

<p>Complexity: {result.estimated_complexity}</p>
<CallGraph graph={result.call_graph} />

        </div>
      )}

    </div>
  )
}
