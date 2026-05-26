import { useState } from "react"
import axios from "axios"
import { useNavigate } from "react-router-dom"

function Login() {

  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

  const navigate = useNavigate()

  const handleLogin = async () => {

    try {

      const formData = new URLSearchParams()

      formData.append("username", email)
      formData.append("password", password)
      formData.append("grant_type", "password")

      const response = await axios.post(
        "http://127.0.0.1:8000/login",
        formData,
        {
          headers: {
            "Content-Type":
              "application/x-www-form-urlencoded"
          }
        }
      )

      console.log(response.data)

      if (
        response.data &&
        response.data.access_token
      ) {

        localStorage.setItem(
          "token",
          response.data.access_token
        )

        alert("Login successful")

        navigate("/dashboard")

      } else {

        alert(
          JSON.stringify(response.data)
        )
      }

    } catch (error) {

      console.log(error)

      alert("Login failed")
    }
  }

  return (

    <div style={{ padding: "40px" }}>

      <h1>MediCheck AI Login</h1>

      <br />

      <input
        type="email"
        placeholder="Enter Email"
        onChange={(e) =>
          setEmail(e.target.value)
        }
        style={{
          padding: "10px",
          width: "300px"
        }}
      />

      <br /><br />

      <input
        type="password"
        placeholder="Enter Password"
        onChange={(e) =>
          setPassword(e.target.value)
        }
        style={{
          padding: "10px",
          width: "300px"
        }}
      />

      <br /><br />

      <button
        onClick={handleLogin}
        style={{
          padding: "10px 20px"
        }}
      >
        Login
      </button>

      <br /><br />

      <a href="/signup">
        Create Account
      </a>

    </div>
  )
}

export default Login