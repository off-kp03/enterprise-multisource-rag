"use client";

type Props = {
  mode: "login" | "signup";
  left: React.ReactNode;
  right: React.ReactNode;
};

export default function AuthShell({ mode, left, right }: Props) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-neutral-950 via-neutral-900 to-neutral-800">
      <div className="relative w-[900px] h-[520px] bg-white rounded-xl shadow-[0_30px_80px_rgba(0,0,0,0.6)] overflow-hidden">

        {/* LEFT PANEL */}
        <div
          className={`
            absolute top-0 left-0 h-full w-1/2
            transition-transform duration-700 ease-in-out
            ${mode === "signup" ? "translate-x-full" : "translate-x-0"}
          `}
        >
          <div className="h-full flex items-center justify-center px-10">
            {left}
          </div>
        </div>

        {/* RIGHT PANEL */}
        <div
          className={`
            absolute top-0 right-0 h-full w-1/2
            bg-gradient-to-br from-neutral-900 via-neutral-800 to-stone-800
            text-white
            transition-transform duration-700 ease-in-out
            ${mode === "signup" ? "-translate-x-full" : "translate-x-0"}
          `}
        >
          <div className="h-full flex items-center justify-center px-10">
            {right}
          </div>
        </div>

      </div>
    </div>
  );
}
