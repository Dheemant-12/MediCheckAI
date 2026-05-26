import { useState } from "react"
import axios from "axios"

function Signup() {

  const [username, setUsername] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

  const handleSignup = async () => {

    try {

      const response = await axios.post(
        "http://127.0.0.1:8000/signup",
        {
          username,
          email,
          password
        }
      )

      if (response.data.message) {

        alert(response.data.message)

        window.location.href = "/"
      }

      if (response.data.error) {

        alert(response.data.error)
      }

    } catch (error) {

      console.log(error)

      alert("Signup failed")
    }
  }

  return (

    <div
      style={{
        padding: "40px",
        fontFamily: "Arial"
      }}
    >

      <h1>MediCheck AI Signup</h1>

      <p>
        Create your account to access
        AI-powered symptom analysis.
      </p>

      <br />

      <label>
        Username
      </label>

      <br />

      <input
        type="text"
        placeholder="Enter unique username"
        onChange={(e) =>
          setUsername(e.target.value)
        }
        style={{
          width: "300px",
          padding: "10px"
        }}
      />

      <br /><br />

      <label>
        Email
      </label>

      <br />

      <input
        type="email"
        placeholder="Enter your email"
        onChange={(e) =>
          setEmail(e.target.value)
        }
        style={{
          width: "300px",
          padding: "10px"
        }}
      />

      <br /><br />

      <label>
        Password
      </label>

      <br />

      <input
        type="password"
        placeholder="Enter secure password"
        onChange={(e) =>
          setPassword(e.target.value)
        }
        style={{
          width: "300px",
          padding: "10px"
        }}
      />

      <br /><br />

      <button
        onClick={handleSignup}
        style={{
          padding: "10px 20px",
          cursor: "pointer"
        }}
      >
        Create Account
      </button>

      <br /><br />

      <a href="/">
        Already have an account? Login
      </a>

    </div>
  )
}

export default Signup