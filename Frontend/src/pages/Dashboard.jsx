import { useState } from "react"
import axios from "axios"

function Dashboard() {

  const [symptoms, setSymptoms] =
    useState("")

  const [analysis, setAnalysis] =
    useState("")

  const handleAnalyze = async () => {

    try {

      console.log("Sending request...")

      const response = await axios.post(
        "http://127.0.0.1:8000/analyze",
        {
          symptoms: symptoms
        }
      )

      console.log(response.data)

      setAnalysis(
        response.data.analysis
      )

    } catch (error) {

      console.log(error)

      alert("AI analysis failed")
    }
  }

  return (

    <div style={{ padding: "40px" }}>

      <h1>MediCheck AI Dashboard</h1>

      <h3>Enter Symptoms</h3>

      <textarea
        rows="5"
        cols="60"
        placeholder="Example: fever, cough, headache"
        value={symptoms}
        onChange={(e) =>
          setSymptoms(e.target.value)
        }
      />

      <br /><br />

      <button onClick={handleAnalyze}>
        Analyze Symptoms
      </button>

      <br /><br />

      <h2>AI Analysis</h2>

      <textarea
        rows="15"
        cols="80"
        value={analysis}
        readOnly
      />

    </div>
  )
}

export default Dashboard