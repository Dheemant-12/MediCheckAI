import {
  Routes,
  Route,
  Navigate
} from "react-router-dom"

import Login from "./pages/Login"
import Signup from "./pages/Signup"
import Dashboard from "./pages/Dashboard"
import Profile from "./pages/Profile"
import RAG from "./pages/RAG"
function ProtectedRoute({ children }) {

  const token =
    localStorage.getItem("token")

  return token
    ? children
    : <Navigate to="/" />
}

function App() {

  return (

    <Routes>

      <Route
        path="/"
        element={<Login />}
      />

      <Route
        path="/signup"
        element={<Signup />}
      />

      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        }
      />
      <Route
        path="/profile"
        element={<Profile />}
      />
      <Route

        path="/rag"

        element={<RAG />}

      />

    </Routes>

  )
}

export default App