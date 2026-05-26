function Dashboard() {

  const token = localStorage.getItem(
    "token"
  )

  const handleLogout = () => {

    localStorage.removeItem("token")

    window.location.href = "/"
  }

  return (

    <div style={{ padding: "40px" }}>

      <h1>MediCheck AI Dashboard</h1>

      <p>
        Authentication successful
      </p>

      <br />

      <h3>Stored JWT Token:</h3>

      <textarea
        rows="10"
        cols="80"
        value={token || "No token found"}
        readOnly
      />

      <br /><br />

      <button
        onClick={handleLogout}
      >
        Logout
      </button>

    </div>
  )
}

export default Dashboard