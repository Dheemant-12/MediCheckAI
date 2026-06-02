import { useState, useEffect } from "react"
import axios from "axios"

function Dashboard() {

  const [symptoms, setSymptoms] = useState("")
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)

  const token = localStorage.getItem("token")

  useEffect(() => {

    loadHistory()

  }, [])

  const loadHistory = async () => {

    try {

      const response = await axios.get(
        "http://127.0.0.1:8000/history",
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

      const historyMessages = []

      response.data.forEach((chat) => {

        historyMessages.push({
          role: "user",
          content: chat.user_message
        })

        historyMessages.push({
          role: "ai",
          content: chat.ai_response
        })

      })

      setMessages(historyMessages)

    } catch (error) {

      console.error(error)

    }

  }

  const clearHistory = async () => {

    try {

      await axios.delete(
        "http://127.0.0.1:8000/history",
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

      setMessages([])

      alert(
        "History cleared successfully"
      )

    } catch (error) {

      console.error(error)

      alert(
        "Failed to clear history"
      )

    }

  }

  const handleAnalyze = async () => {

    if (!symptoms.trim()) return

    const userMessage = {
      role: "user",
      content: symptoms
    }

    setMessages(prev => [
      ...prev,
      userMessage
    ])

    setLoading(true)

    try {

      const response = await axios.post(
        "http://127.0.0.1:8000/analyze",
        {
          symptoms
        },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

      const aiMessage = {
        role: "ai",
        content: response.data.analysis
      }

      setMessages(prev => [
        ...prev,
        aiMessage
      ])

      setSymptoms("")

    } catch (error) {

      console.error(error)

      const aiError = {
        role: "ai",
        content:
          "Sorry, something went wrong while analyzing symptoms."
      }

      setMessages(prev => [
        ...prev,
        aiError
      ])

    } finally {

      setLoading(false)

    }

  }

  return (

    <div
      style={{
        background: "#f4f6f8",
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        padding: "30px"
      }}
    >

      <div
        style={{
          width: "900px"
        }}
      >

        <h1>🩺 MediCheck AI</h1>

        <button
          onClick={() => {

            localStorage.removeItem(
              "token"
            )

            window.location.href = "/"

          }}
          style={{
            padding: "10px 15px",
            cursor: "pointer",
            marginBottom: "15px"
          }}
        >
          Logout
        </button>

        <p>
          Describe your symptoms and receive AI-powered guidance.
        </p>

        <button
          onClick={() => setMessages([])}
          style={{
            padding: "10px 15px",
            marginBottom: "15px",
            cursor: "pointer"
          }}
        >
          New Chat
        </button>

        <button
          onClick={clearHistory}
          style={{
            padding: "10px 15px",
            marginLeft: "10px",
            marginBottom: "15px",
            cursor: "pointer"
          }}
        >
          Clear History
        </button>

        <div
          style={{
            background: "white",
            borderRadius: "12px",
            padding: "20px",
            height: "500px",
            overflowY: "auto",
            border: "1px solid #ddd"
          }}
        >

          {messages.length === 0 && (

            <div>

              <h3>
                No previous conversations
              </h3>

            </div>

          )}

          {messages.map((msg, index) => (

            <div
              key={index}
              style={{
                display: "flex",
                justifyContent:
                  msg.role === "user"
                    ? "flex-end"
                    : "flex-start",
                marginBottom: "15px"
              }}
            >

              <div
                style={{
                  maxWidth: "75%",
                  padding: "12px",
                  borderRadius: "12px",
                  whiteSpace: "pre-wrap",
                  backgroundColor:
                    msg.role === "user"
                      ? "#007bff"
                      : "#eeeeee",
                  color:
                    msg.role === "user"
                      ? "white"
                      : "black"
                }}
              >

                {msg.content}

              </div>

            </div>

          ))}

          {loading && (

            <div>

              🤖 MediCheck AI is analyzing...

            </div>

          )}

        </div>

        <div
          style={{
            marginTop: "20px"
          }}
        >

          <textarea
            rows="4"
            placeholder="Describe your symptoms..."
            value={symptoms}
            onChange={(e) =>
              setSymptoms(e.target.value)
            }
            style={{
              width: "100%",
              padding: "12px",
              fontSize: "16px"
            }}
          />

          <br />
          <br />

          <button
            onClick={handleAnalyze}
            disabled={loading}
            style={{
              padding: "12px 20px",
              cursor: "pointer"
            }}
          >
            Send
          </button>

        </div>

      </div>

    </div>

  )
}

export default Dashboard