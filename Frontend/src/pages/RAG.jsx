import { useState } from "react"
import axios from "axios"

function RAG() {

  const [file, setFile] = useState(null)
  const [message, setMessage] = useState("")

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

    </div>

  )

}

export default RAG