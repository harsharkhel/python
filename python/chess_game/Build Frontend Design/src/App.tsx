import { useState } from "react";
import svgPaths from "@/imports/PremiumEliteFocusVariant/svg-1hagu0eg0y";
import imgChess from "@/imports/PremiumEliteFocusVariant/c654f55e054bdd0de6110c2a915c960b3fa0c1ff.png";
import imgLogo from "@/imports/PremiumEliteFocusVariant/3005ba738e7d530f7750f4797d787caed1a14ba0.png";

function GoogleIcon() {
  return (
    <svg fill="none" height="20" viewBox="0 0 20 20" width="20">
      <path d={svgPaths.p29ad9380} fill="#4285F4" />
      <path d={svgPaths.p73c0a80} fill="#34A853" />
      <path d={svgPaths.p1f69ba00} fill="#FBBC05" />
      <path d={svgPaths.p3d0b3f00} fill="#EA4335" />
    </svg>
  );
}

function LinkedInIcon() {
  return (
    <svg fill="none" height="20" viewBox="0 0 20 20" width="20">
      <g clipPath="url(#li-clip)">
        <path d={svgPaths.p68ec00} fill="#0A66C2" />
      </g>
      <defs>
        <clipPath id="li-clip">
          <rect fill="white" height="20" width="20" />
        </clipPath>
      </defs>
    </svg>
  );
}

export default function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [remember, setRemember] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // sign-in handler placeholder
  };

  return (
    <div
      className="flex items-center justify-center p-8 min-h-screen w-full"
      style={{ background: "linear-gradient(90deg, #0a0a0a 0%, #0a0a0a 100%)" }}
    >
      {/* Card */}
      <div className="relative rounded-xl w-full max-w-5xl shadow-[0px_25px_50px_-12px_rgba(0,0,0,0.25)] flex overflow-hidden" style={{ minHeight: 600 }}>
        {/* Border overlay */}
        <div className="absolute inset-0 border border-[#222] rounded-xl pointer-events-none z-10" />

        {/* Left — hero image */}
        <div className="relative flex-1 min-w-0 bg-black hidden md:block">
          <img
            alt="Golden chess king on board"
            className="absolute inset-0 w-full h-full object-cover object-center opacity-90"
            src={imgChess}
            style={{ objectPosition: "60% center" }}
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent" />
        </div>

        {/* Right — form */}
        <div className="flex-1 min-w-0 bg-[#111] flex flex-col justify-center">
          <form
            onSubmit={handleSubmit}
            className="flex flex-col items-start gap-0 px-10 py-16 w-full max-w-[448px] mx-auto"
          >
            {/* Logo */}
            <img
              alt="Castle"
              src={imgLogo}
              className="size-16 opacity-90 shrink-0"
            />

            {/* Heading */}
            <h1
              className="mt-6 text-[30px] font-bold tracking-[-0.75px] text-[#e0e0e0] leading-[36px] w-full"
              style={{ fontFamily: "Inter, sans-serif" }}
            >
              Sign In
            </h1>

            {/* Subheading */}
            <p
              className="mt-2 text-[14px] font-light text-[#c0c0c0] leading-5"
              style={{ fontFamily: "Inter, sans-serif" }}
            >
              Welcome back to the strategic platform.
            </p>

            {/* Email field */}
            <div className="mt-6 flex flex-col gap-2 w-full">
              <label
                htmlFor="email"
                className="text-[14px] font-medium text-[#c0c0c0] leading-5"
                style={{ fontFamily: "Inter, sans-serif" }}
              >
                Email Address
              </label>
              <div className="relative rounded-[6px] w-full">
                <div className="absolute bg-[#1e1e1e] inset-0 rounded-[6px] pointer-events-none" />
                <div className="absolute inset-0 border border-[#333] rounded-[6px] pointer-events-none shadow-[inset_0px_2px_4px_1px_rgba(0,0,0,0.05)]" />
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="you@company.com"
                  className="relative w-full bg-transparent px-[17px] py-[15px] text-[16px] text-[#e0e0e0] placeholder:text-[#6b7280] outline-none rounded-[6px]"
                  style={{ fontFamily: "Inter, sans-serif" }}
                  autoComplete="email"
                />
              </div>
            </div>

            {/* Password field */}
            <div className="mt-6 flex flex-col gap-2 w-full">
              <label
                htmlFor="password"
                className="text-[14px] font-medium text-[#c0c0c0] leading-5"
                style={{ fontFamily: "Inter, sans-serif" }}
              >
                Password
              </label>
              <div className="relative rounded-[6px] w-full">
                <div className="absolute bg-[#1e1e1e] inset-0 rounded-[6px] pointer-events-none" />
                <div className="absolute inset-0 border border-[#333] rounded-[6px] pointer-events-none shadow-[inset_0px_2px_4px_1px_rgba(0,0,0,0.05)]" />
                <input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="relative w-full bg-transparent px-[17px] py-[15px] text-[16px] text-[#e0e0e0] placeholder:text-[#6b7280] outline-none rounded-[6px]"
                  style={{ fontFamily: "Inter, sans-serif" }}
                  autoComplete="current-password"
                />
              </div>
            </div>

            {/* Remember me + Forgot */}
            <div className="mt-6 flex items-center justify-between w-full">
              <label className="flex items-center gap-2 cursor-pointer">
                <div
                  className="relative size-4 rounded-[4px] bg-[#1e1e1e] border border-[#333] shrink-0 flex items-center justify-center cursor-pointer"
                  onClick={() => setRemember(!remember)}
                >
                  {remember && (
                    <svg viewBox="0 0 10 10" className="size-2.5" fill="none">
                      <path d="M1.5 5l2.5 2.5 4.5-4.5" stroke="#cda434" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                  )}
                  <input
                    type="checkbox"
                    checked={remember}
                    onChange={(e) => setRemember(e.target.checked)}
                    className="sr-only"
                  />
                </div>
                <span
                  className="text-[14px] font-normal text-[#c0c0c0] leading-5 select-none"
                  style={{ fontFamily: "Inter, sans-serif" }}
                >
                  Remember me
                </span>
              </label>
              <button
                type="button"
                className="text-[14px] font-medium text-[#cda434] leading-5 hover:text-[#e6c86a] transition-colors"
                style={{ fontFamily: "Inter, sans-serif" }}
              >
                Forgot password?
              </button>
            </div>

            {/* Sign In button */}
            <button
              type="submit"
              className="mt-6 w-full relative rounded-[6px] overflow-hidden group"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-[#cda434] via-[#e6c86a] to-[#cda434] rounded-[6px]" />
              <div className="absolute inset-0 bg-white/0 group-hover:bg-white/10 transition-colors rounded-[6px]" />
              <div className="relative px-[17px] py-[13px] shadow-[0px_4px_6px_-1px_rgba(0,0,0,0.1),0px_2px_4px_-2px_rgba(0,0,0,0.1)]">
                <span
                  className="text-[14px] font-semibold text-black tracking-wide"
                  style={{ fontFamily: "Inter, sans-serif" }}
                >
                  SIGN IN
                </span>
              </div>
            </button>

            {/* Divider */}
            <div className="mt-6 relative flex items-center w-full">
              <div className="flex-1 border-t border-[#333]" />
              <div className="bg-[#111] px-2">
                <span
                  className="text-[14px] text-[#6b7280]"
                  style={{ fontFamily: "Inter, sans-serif" }}
                >
                  Or continue with
                </span>
              </div>
              <div className="flex-1 border-t border-[#333]" />
            </div>

            {/* OAuth buttons */}
            <div className="mt-6 flex gap-4 w-full">
              <button
                type="button"
                className="flex-1 flex items-center justify-center gap-2 bg-[#1e1e1e] border border-[#333] rounded-[6px] px-4 py-[11px] hover:bg-[#2a2a2a] transition-colors shadow-[0px_1px_1px_rgba(0,0,0,0.05)]"
              >
                <GoogleIcon />
                <span
                  className="text-[14px] font-medium text-[#c0c0c0]"
                  style={{ fontFamily: "Inter, sans-serif" }}
                >
                  Google
                </span>
              </button>
              <button
                type="button"
                className="flex-1 flex items-center justify-center gap-2 bg-[#1e1e1e] border border-[#333] rounded-[6px] px-4 py-[11px] hover:bg-[#2a2a2a] transition-colors shadow-[0px_1px_1px_rgba(0,0,0,0.05)]"
              >
                <LinkedInIcon />
                <span
                  className="text-[14px] font-medium text-[#c0c0c0]"
                  style={{ fontFamily: "Inter, sans-serif" }}
                >
                  LinkedIn
                </span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
