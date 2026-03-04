import axios from "axios"

const API_URL = "http://localhost:8000"

export const analyzeCode = async (code) => {
  const response = await axios.post(`${API_URL}/analyze`, {
    code: code
  })

  return response.data
}