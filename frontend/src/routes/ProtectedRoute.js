import { Navigate } from "react-router-dom";

function ProtectedRoute({ children }) {
  const storedUser = sessionStorage.getItem("user");

  // safely parse
  let user = null;
  try {
    user = storedUser ? JSON.parse(storedUser) : null;
  } catch {
    user = null;
  }
  console.log("ProtectedRoute:", storedUser);

  // proper validation
  if (!user || !user.userId) {
    return <Navigate to="/login" replace />;
  }

  return children;
}

export default ProtectedRoute;
