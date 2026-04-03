import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import login_img from "../images/login_img.png";

function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const navigate = useNavigate();

  // Check if already logged in
  // useEffect(() => {
  //   const user = sessionStorage.getItem("user");
  //   if (user) {
  //     navigate("/new-project", { replace: true });
  //   }
  // }, []);

  // Login handler
  const handleLogin = async () => {
    try {
      const res = await axios.post("http://localhost:8080/auth/login", {
        email: email.trim(),
        password: password.trim(),
      });

      // Store user => session storage
      sessionStorage.setItem("user", JSON.stringify(res.data));

      // Redirect to new project page
      navigate("/new-project", { replace: true });
    } catch (err) {
      console.error(err);
      setError("Invalid email or password");
    }
  };

  return (
    <div className="flex h-screen">
      {/* LEFT SIDE */}
      <div className="w-1/2 bg-gradient-to-br from-[#0F172A] to-[#1E293B] text-white flex flex-col justify-center items-center px-12">
        {/* IMAGE */}
        <img
          src={login_img}
          alt="finance illustration"
          className="w-80 mb-8 drop-shadow-2xl"
        />

        {/* TEXT */}
        <h1 className="text-4xl font-semibold tracking-tight mb-4">
          Cap<span className="text-green-400">Wise</span>
        </h1>

        <p className="text-slate-300 text-center max-w-md text-sm leading-relaxed">
          Make smarter investment decisions using data-driven financial
          modeling, risk analysis, and predictive insights.
        </p>
      </div>

      {/* RIGHT SIDE */}
      <div className="w-1/2 flex justify-center items-center bg-slate-50">
        <div className="bg-white p-10 rounded-2xl shadow-sm border border-slate-200 w-96">
          <h2 className="text-2xl font-semibold text-slate-800 mb-6">
            Welcome back
          </h2>

          {/* Error */}
          {error && <p className="text-red-500 text-sm mb-4">{error}</p>}

          {/* Email */}
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full px-4 py-3 border border-slate-200 rounded-xl mb-4 text-sm focus:outline-none focus:ring-2 focus:ring-slate-300"
          />

          {/* Password */}
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-4 py-3 border border-slate-200 rounded-xl mb-6 text-sm focus:outline-none focus:ring-2 focus:ring-slate-300"
          />

          {/* Button */}
          <button
            onClick={handleLogin}
            disabled={!email || !password}
            className={`w-full py-3 rounded-xl text-sm font-medium transition ${
              email && password
                ? "bg-slate-800 hover:bg-slate-700 text-white"
                : "bg-slate-300 text-white cursor-not-allowed"
            }`}
          >
            Login
          </button>

          {/* Register */}
          <p className="text-sm text-center mt-5 text-slate-500">
            Don’t have an account?{" "}
            <span
              className="text-slate-800 font-medium cursor-pointer hover:underline"
              onClick={() => navigate("/register")}
            >
              Register
            </span>
          </p>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;
