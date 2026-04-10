import { useNavigate } from "react-router-dom";

function WelcomePage() {
  const navigate = useNavigate();

  return (
    <div className="h-screen flex flex-col justify-center items-center bg-gradient-to-br from-[#0F172A] via-[#1E293B] to-[#020617] text-white px-6">
      {/* Logo / Title */}
      <h1 className="text-5xl font-semibold tracking-tight mb-4">
        Cap<span className="text-green-400">Wise</span>
      </h1>

      {/* Subtitle */}
      <p className="text-slate-300 text-center max-w-xl text-lg mb-10">
        Make smarter investment decisions with AI-powered financial modeling,
        risk analysis, and predictive insights.
      </p>

      {/* Buttons */}
      <div className="flex gap-4">
        <button
          onClick={() => navigate("/login")}
          className="px-6 py-3 rounded-xl bg-white text-slate-900 font-medium hover:bg-slate-200 transition"
        >
          Login
        </button>

        <button
          onClick={() => navigate("/register")}
          className="px-6 py-3 rounded-xl border border-slate-400 text-white font-medium hover:bg-slate-800 transition"
        >
          Register
        </button>
      </div>

      {/* Footer note */}
      <p className="absolute bottom-6 text-xs text-slate-500">
        Built for smarter financial decisions 
      </p>
    </div>
  );
}

export default WelcomePage;
