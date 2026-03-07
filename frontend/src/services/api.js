export async function analyzeCode(code, language) {

  const res = await fetch("http://127.0.0.1:8000/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      code: code,
      language: language
    })
  })

  return res.json()
}