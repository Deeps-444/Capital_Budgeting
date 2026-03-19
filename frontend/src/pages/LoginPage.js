import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const navigate = useNavigate();

  //  Redirect if already logged in
  useEffect(() => {
    const user = JSON.parse(sessionStorage.getItem("user"));
    if (user) {
      navigate("/", { replace: true });
    }
  }, [navigate]);

  //  Login handler
  const handleLogin = async () => {
    try {
      const res = await axios.post("http://localhost:8080/login", {
        email: email.trim(),
        password: password.trim(),
      });

      // store user
      sessionStorage.setItem("user", JSON.stringify(res.data));

      // redirect to main page
      navigate("/", { replace: true });
    } catch (err) {
      console.error(err);
      setError("Invalid email or password");
    }
  };

  return (
    <div style={{ padding: "30px" }}>
      <h2>Login</h2>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <input
        type="email"
        placeholder="Enter email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <br />
      <br />

      <input
        type="password"
        placeholder="Enter password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <br />
      <br />

      <button onClick={handleLogin} disabled={!email || !password}>
        Login
      </button>
    </div>
  );
}

export default LoginPage;
