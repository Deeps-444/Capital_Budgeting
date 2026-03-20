import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const navigate = useNavigate();

  // Redirect if already logged in
  useEffect(() => {
    const user = JSON.parse(sessionStorage.getItem("user"));
    if (user) {
      navigate("/", { replace: true });
    }
  }, [navigate]);

  // Login handler
  const handleLogin = async () => {
    try {
      const res = await axios.post("http://localhost:8080/login", {
        email: email.trim(),
        password: password.trim(),
      });

      sessionStorage.setItem("user", JSON.stringify(res.data));
      navigate("/", { replace: true });
    } catch (err) {
      console.error(err);
      setError("Invalid email or password");
    }
  };

  return (
    <div className="flex h-screen">
      {/* 🔷 LEFT SIDE (Branding) */}
      <div className="w-1/2 bg-gradient-to-br from-[#0F172A] to-[#1E293B] text-white flex flex-col justify-center items-center px-10">
        <h1 className="text-4xl font-bold text-green-400 mb-4">Random Name</h1>

        <p className="text-gray-300 text-center max-w-md">
          Smart Capital Budgeting Descision Support System.
        </p>
      </div>

      {/*RIGHT SIDE (Form) */}
      <div className="w-1/2 flex justify-center items-center bg-[#F8FAFC]">
        <div className="bg-white p-8 rounded-xl shadow-md w-96">
          <h2 className="text-2xl font-bold mb-6 text-gray-800">
            Welcome Back 👋
          </h2>

          {/* Error */}
          {error && <p className="text-red-500 text-sm mb-4">{error}</p>}

          {/* Email */}
          <input
            type="email"
            placeholder="Enter email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full p-3 border rounded-lg mb-4 focus:outline-none focus:ring-2 focus:ring-green-400"
          />

          {/* Password */}
          <input
            type="password"
            placeholder="Enter password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full p-3 border rounded-lg mb-6 focus:outline-none focus:ring-2 focus:ring-green-400"
          />

          {/* 🔘 Button */}
          <button
            onClick={handleLogin}
            disabled={!email || !password}
            className={`w-full p-3 rounded-lg text-white transition ${
              email && password
                ? "bg-green-500 hover:bg-green-600"
                : "bg-gray-400 cursor-not-allowed"
            }`}
          >
            Login
          </button>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;
