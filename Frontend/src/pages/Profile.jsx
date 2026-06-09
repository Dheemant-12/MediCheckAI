import { useState, useEffect }
from "react"

import axios from "axios"

function Profile() {

  const [profile,
    setProfile] = useState(null)

  const token =
    localStorage.getItem(
      "token"
    )

  useEffect(() => {

    loadProfile()

  }, [])

  const loadProfile =
  async () => {

    try {

      const response =
        await axios.get(
          "http://127.0.0.1:8000/profile",
          {
            headers: {
              Authorization:
                `Bearer ${token}`
            }
          }
        )

      setProfile(
        response.data
      )

    } catch (error) {

      console.error(error)

    }

  }

  if (!profile) {

    return <h2>Loading...</h2>

  }

  return (

    <div
      style={{
        padding: "40px"
      }}
    >

      <h1>
        👤 Profile
      </h1>

      <h3>
        Username:
        {profile.username}
      </h3>

      <h3>
        Email:
        {profile.email}
      </h3>

      <hr />

      <h2>
        Statistics
      </h2>

      <h3>
        Conversations:
        {profile.total_sessions}
      </h3>

      <h3>
        Messages:
        {profile.total_messages}
      </h3>

    </div>

  )

}

export default Profile