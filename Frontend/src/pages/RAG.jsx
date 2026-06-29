import { useState } from "react"
import axios from "axios"

function RAG() {

  const [file, setFile] = useState(null)

  const [message, setMessage] = useState("")

  const [question, setQuestion] = useState("")

  const [answer, setAnswer] = useState("")
  const [sourcePreview, setSourcePreview] = useState("")
  const [chunksUsed, setChunksUsed] = useState(0)
  const token = localStorage.getItem("token")

  const uploadPDF = async () => {

    if (!file) {

      alert("Select a PDF first")

      return

    }

    const formData = new FormData()

    formData.append(
      "file",
      file
    )

    try {

      const response =
        await axios.post(

          "http://127.0.0.1:8000/upload-pdf",

          formData,

          {

            headers: {

              Authorization:
                `Bearer ${token}`,

              "Content-Type":
                "multipart/form-data"

            }

          }

        )

      setMessage(
        response.data.message
      )

    }

    catch (error) {

      console.error(error)

    }

  }

  const askPDF = async () => {

    if (!question) {

      alert("Enter a question")

      return

    }

    try {

      const response =
        await axios.post(

          "http://127.0.0.1:8000/ask-pdf",

          {

            question

          },

          {

            headers: {

              Authorization:
                `Bearer ${token}`

            }

          }

        )

      setAnswer(
        response.data.answer
      )
      setSourcePreview(
        response.data.source_preview
      )

      setChunksUsed(
        response.data.chunks_used
      )

    }

    catch (error) {

      console.error(error)

    }

  }

  return (

    <div
      style={{
        padding: "40px"
      }}
    >

      <h1>
        Medical Knowledge Base
      </h1>

      <input

        type="file"

        accept=".pdf"

        onChange={(e) =>
          setFile(
            e.target.files[0]
          )
        }

      />

      <br /><br />

      <button
        onClick={uploadPDF}
      >

        Upload PDF

      </button>

      <h3>

        {message}

      </h3>

      <br />

      <textarea

        placeholder="Ask something about the uploaded PDF..."

        rows={5}

        cols={70}

        value={question}

        onChange={(e) =>
          setQuestion(
            e.target.value
          )
        }

      />

      <br /><br />

      <button
        onClick={askPDF}
      >

        Ask PDF

      </button>

      <br /><br />

      <div
        style={{
          border: "1px solid #ddd",
          padding: "20px",
          borderRadius: "10px",
          minHeight: "120px",
          whiteSpace: "pre-wrap"
        }}
      >

        <strong>

          AI Answer

        </strong>

        <br /><br />

        {answer}

        <hr />

        <strong>

          📄 Source

        </strong>

        <br /><br />

        <b>

          Chunks Used:

        </b>

        {" "}

        {chunksUsed}

        <br /><br />

        <b>

          Preview:

        </b>

        <br />

        {sourcePreview}

      </div>

        <strong>
          AI Answer
        </strong>

        <br /><br />

        {answer}

      </div>

    

  )

}

export default RAG