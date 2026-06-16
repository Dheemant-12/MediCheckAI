import { useState, useEffect }
from "react"

import axios from "axios"

function Profile() {

  const [profile,
    setProfile] = useState(null)
  const [timeline,
    setTimeline] = useState([])
  const [trends,
    setTrends] = useState([])  
  const [insights,
    setInsights] = useState([])
  const token =
    localStorage.getItem(
      "token"
    )

  useEffect(() => {

  loadProfile()

  loadTimeline()

  loadTrends()

  loadInsights()

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


const loadTimeline =
async () => {

  try {

    const response =
      await axios.get(
        "http://127.0.0.1:8000/timeline",
        {
          headers: {
            Authorization:
              `Bearer ${token}`
          }
        }
      )

    setTimeline(
      response.data
    )

  } catch (error) {

    console.error(error)

  }

}


const loadTrends =
async () => {

  try {

    const response =
      await axios.get(
        "http://127.0.0.1:8000/symptom-trends",
        {
          headers: {
            Authorization:
              `Bearer ${token}`
          }
        }
      )

    setTrends(
      response.data
    )

  } catch (error) {

    console.error(error)

  }

}
const loadInsights =
async () => {

  try {

    const response =
      await axios.get(
        "http://127.0.0.1:8000/health-insights",
        {
          headers: {
            Authorization:
              `Bearer ${token}`
          }
        }
      )

    setInsights(
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
      padding: "40px",
      maxWidth: "700px",
      margin: "0 auto"
    }}
  >
      <button
        onClick={() =>
          window.location.href =
          "/dashboard"
        }
        style={{
          padding: "10px 15px",
          cursor: "pointer"
        }}
      >
        ← Dashboard
      </button>
      <h1>
        👤 Profile
      </h1>
      <div
        style={{
          background: "white",
          padding: "20px",
          borderRadius: "12px",
          border: "1px solid #ddd",
          marginTop: "20px"
        }}
      ></div>

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

      <h3>
        Average Messages:
        {profile.average_messages}
      </h3>

      <h3>
        Most Active Chat:
        {profile.most_active}
      </h3>

      <hr />
      <hr />

      <h2>
        Health Insights
      </h2>

      {insights.map((item, index) => (

        <div
          key={index}
          style={{
            padding: "10px",
            border: "1px solid #ddd",
            borderRadius: "8px",
            marginBottom: "10px",
            background: "#f8f9fa"
          }}
        >

          • {item}

        </div>

      ))}

      <h2>
        Symptom Trends
      </h2>

      {trends.map((item) => (

        <div
          key={item.symptom}
          style={{
            padding: "10px",
            border: "1px solid #ddd",
            borderRadius: "8px",
            marginBottom: "10px"
          }}
        >

          {item.symptom}
          {" : "}
          {item.count}

        </div>

      ))}

      <hr />

      <h2>
        Medical Timeline
      </h2>

      {timeline.map((item) => (

        <div
          key={item.id}
          style={{
            padding: "10px",
            border: "1px solid #ddd",
            borderRadius: "8px",
            marginBottom: "10px"
          }}
        >

          {item.title}

        </div>

      ))}
      </div>


  )

}

export default Profile