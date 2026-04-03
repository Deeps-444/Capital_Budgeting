import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import register_img from "../images/register_img.png";

function RegisterPage() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleRegister = async (e) => {
    e.preventDefault();

    try {
      const res = await axios.post(
        "http://localhost:8080/auth/register",
        formData,
      );

      alert("Registration successful!");
      navigate("/login");
    } catch (err) {
      console.error(err);
      alert("Registration failed");
    }
  };

  return (
    <div className="flex h-screen">
      {/* LEFT SIDE */}
      <div className="w-1/2 bg-gradient-to-br from-[#0F172A] to-[#1E293B] text-white flex flex-col justify-center items-center px-12">
        {/* IMAGE */}
        <img
          src={register_img}
          alt="signup illustration"
          className="w-80 mb-8 drop-shadow-2xl"
        />

        {/* TEXT */}
        <h1 className="text-4xl font-semibold tracking-tight mb-4">
          Cap<span className="text-green-400">Wise</span>
        </h1>

        <p className="text-slate-300 text-center max-w-md text-sm leading-relaxed">
          Create an account to start analyzing investment opportunities with
          intelligent financial insights.
        </p>
      </div>

      {/* RIGHT SIDE */}
      <div className="w-1/2 flex justify-center items-center bg-slate-50">
        <form
          onSubmit={handleRegister}
          className="bg-white p-10 rounded-2xl shadow-sm border border-slate-200 w-96"
        >
          <h2 className="text-2xl font-semibold text-slate-800 mb-6">
            Create account
          </h2>

          {/* Name */}
          <input
            type="text"
            name="name"
            placeholder="Full Name"
            className="w-full px-4 py-3 border border-slate-200 rounded-xl mb-4 text-sm focus:outline-none focus:ring-2 focus:ring-slate-300"
            onChange={handleChange}
            required
          />

          {/* Email */}
          <input
            type="email"
            name="email"
            placeholder="Email"
            className="w-full px-4 py-3 border border-slate-200 rounded-xl mb-4 text-sm focus:outline-none focus:ring-2 focus:ring-slate-300"
            onChange={handleChange}
            required
          />

          {/* Password */}
          <input
            type="password"
            name="password"
            placeholder="Password"
            className="w-full px-4 py-3 border border-slate-200 rounded-xl mb-6 text-sm focus:outline-none focus:ring-2 focus:ring-slate-300"
            onChange={handleChange}
            required
          />

          {/* Button */}
          <button
            type="submit"
            className="w-full py-3 rounded-xl text-sm font-medium bg-slate-800 text-white hover:bg-slate-700 transition"
          >
            Register
          </button>

          {/* Login */}
          <p className="text-sm text-center mt-5 text-slate-500">
            Already have an account?{" "}
            <span
              className="text-slate-800 font-medium cursor-pointer hover:underline"
              onClick={() => navigate("/login")}
            >
              Login
            </span>
          </p>
        </form>
      </div>
    </div>
  );
}

export default RegisterPage;
