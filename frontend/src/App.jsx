import { useState } from "react"
import { analyzeCode } from "./services/api"

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

          <p>Loops: {result.loops}</p>
          <p>Functions: {result.functions.join(", ")}</p>
          <p>Complexity: {result.estimated_complexity}</p>

        </div>
      )}

    </div>
  )
}