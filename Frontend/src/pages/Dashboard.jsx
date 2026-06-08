import { useState, useEffect,useRef } from "react"
import axios from "axios"

function Dashboard() {

  const [symptoms, setSymptoms] = useState("")
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)

  const [sessions, setSessions] = useState([])
  const [searchTerm,setSearchTerm] = useState("")


  const [selectedSession,
    setSelectedSession] = useState(null)
  const messagesEndRef =useRef(null)  
  const [editingSession,
    setEditingSession] = useState(null)  
  const token = localStorage.getItem("token")

  useEffect(() => {

    loadSessions()

  }, [])
  useEffect(() => {

    messagesEndRef.current
      ?.scrollIntoView({
        behavior: "smooth"
      })

  }, [messages])

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
  const loadSessions = async () => {

    try {

      const response = await axios.get(
        "http://127.0.0.1:8000/sessions",
        {
          headers: {
            Authorization:
              `Bearer ${token}`
          }
        }
      )

      setSessions(
        response.data
      )

    } catch (error) {

      console.error(error)

    }

  }
  const loadSessionHistory =
  async (sessionId) => {

    try {

      const response =
        await axios.get(
          `http://127.0.0.1:8000/session/${sessionId}/history`,
          {
            headers: {
              Authorization:
                `Bearer ${token}`
            }
          }
        )

      const historyMessages = []

      response.data.forEach(
        (chat) => {

          historyMessages.push({
            role: "user",
            content:
              chat.user_message
          })

          historyMessages.push({
            role: "ai",
            content:
              chat.ai_response
          })

        }
      )

      setSelectedSession(
        sessionId
      )

      setMessages(
        historyMessages
      )

    } catch (error) {

      console.error(error)

    }

  }
  const createSession = async () => {

  try {

    const response =
      await axios.post(
        "http://127.0.0.1:8000/session",
        {
          title:
            "New Conversation"
        },
        {
          headers: {
            Authorization:
              `Bearer ${token}`
          }
        }
      )

    await loadSessions()

    setSelectedSession(
      response.data.session_id
    )

    setMessages([])

  } catch (error) {

    console.error(error)

  }

}
  const deleteSession =
  async (sessionId) => {
    const confirmDelete =
      window.confirm(
        "Delete this conversation?"
      )

    if (!confirmDelete) {

      return

    }

    try {

      await axios.delete(
        `http://127.0.0.1:8000/session/${sessionId}`,
        {
          headers: {
            Authorization:
              `Bearer ${token}`
          }
        }
      )

      if (
        selectedSession ===
        sessionId
      ) {

        setSelectedSession(
          null
        )

        setMessages([])

      }

      await loadSessions()

    } catch (error) {

      console.error(error)

    }

  }
  const renameSession =
  async (sessionId) => {

    const newTitle = prompt(
      "Enter new title"
    )

    if (!newTitle) return

    try {

      await axios.put(
        `http://127.0.0.1:8000/session/${sessionId}`,
        {
          title: newTitle
        },
        {
          headers: {
            Authorization:
              `Bearer ${token}`
          }
        }
      )

      await loadSessions()

    } catch (error) {

      console.error(error)

    }

  }
  const exportPdf =
  async () => {

    if (!selectedSession) {

      alert(
        "Select a conversation first"
      )

      return

    }

    try {

      const response =
        await axios.get(
          `http://127.0.0.1:8000/session/${selectedSession}/pdf`,
          {
            headers: {
              Authorization:
                `Bearer ${token}`
            },
            responseType:
              "blob"
          }
        )

      const url =
        window.URL.createObjectURL(
          new Blob([response.data])
        )

      const link =
        document.createElement("a")

      link.href = url

      link.setAttribute(
        "download",
        `session_${selectedSession}.pdf`
      )

      document.body.appendChild(
        link
      )

      link.click()

      link.remove()

    } catch (error) {

      console.error(error)

      alert(
        "Failed to export PDF"
      )

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
    if (!selectedSession) {

      alert(
        "Please select or create a conversation first."
      )

      return

    }
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
          session_id:
            selectedSession,
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

      if (
        messages.length === 0
      ) {

        const title =
          symptoms
            .split(" ")
            .slice(0, 4)
            .join(" ")

        await axios.put(
          `http://127.0.0.1:8000/session/${selectedSession}`,
          {
            title
          },
          {
            headers: {
              Authorization:
                `Bearer ${token}`
            }
          }
        )

        await loadSessions()

      }

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
          width: "1200px",
          display: "flex",
          gap: "20px"
        }}
      >
      <div
        style={{
          width: "250px",
          background: "white",
          padding: "15px",
          borderRadius: "12px",
          border: "1px solid #ddd"
        }}
      >

        <h3>
          Conversations
        </h3>
        <input
          type="text"
          placeholder="Search..."
          value={searchTerm}
          onChange={(e) =>
            setSearchTerm(
              e.target.value
            )
          }
          style={{
            width: "100%",
            padding: "8px",
            marginBottom: "15px",
            borderRadius: "6px",
            border: "1px solid #ddd"
          }}
        />
        {sessions
          .filter((session) =>
            session.title
              .toLowerCase()
              .includes(
                searchTerm.toLowerCase()
              )
          )
          .map((session) => ( 

          <div
            key={session.id}
            style={{
              display: "flex",
              alignItems: "center",
              gap: "10px",
              marginBottom: "10px"
            }}
          >

            <div
              onClick={() =>
                loadSessionHistory(
                  session.id
                )
              }
              style={{
                flex: 1,
                padding: "10px",
                cursor: "pointer",
                border:
                  selectedSession ===
                  session.id
                    ? "2px solid #007bff"
                    : "1px solid #ddd",
                borderRadius: "8px",
                 background:
                  selectedSession ===
                  session.id
                    ? "#e7f1ff"
                    : "white"
              }}
            >

              {session.title}

            </div>

            <button
              onClick={() =>
                deleteSession(
                  session.id
                )
              }
              style={{
                cursor: "pointer"
              }}
            >
              🗑
            </button>
            <button
              onClick={() =>
                renameSession(
                  session.id
                )
              }
              style={{
                cursor: "pointer"
              }}
            >
              ✏️
            </button>  

            </div>

          ))}
      </div>     
      <div
        style={{
          flex: 1
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
          onClick={createSession}
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
        <button
          onClick={exportPdf}
          style={{
            padding: "10px 15px",
            marginLeft: "10px",
            marginBottom: "15px",
            cursor: "pointer"
          }}
        >
          📄 Export PDF
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
          <div
            ref={messagesEndRef}
          />

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
            {loading
              ? "Analyzing..."
              : "Send"}
          </button>

        </div>

      </div>

    </div>
  
  </div>

  )
}

export default Dashboard