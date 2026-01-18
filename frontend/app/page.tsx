"use client";

import { useState } from "react";
import AuthShell from "@/components/AuthShell";
import LoginForm from "@/components/LoginForm";
import SignupForm from "@/components/SignupForm";
import SidePanel from "@/components/SidePanel";

export default function HomePage() {
  const [mode, setMode] = useState<"login" | "signup">("login");

  return (
    <AuthShell
      mode={mode}
      left={
        mode === "login" ? (
          <LoginForm onSwitch={() => setMode("signup")} />
        ) : (
          <SignupForm onSwitch={() => setMode("login")} />
        )
      }
      right={
        mode === "login" ? (
          <SidePanel
            title="New here?"
            subtitle="Create an account to get started"
            buttonText="Sign Up"
            onClick={() => setMode("signup")}
          />
        ) : (
          <SidePanel
            title="Welcome back!"
            subtitle="Login with your existing account"
            buttonText="Login"
            onClick={() => setMode("login")}
          />
        )
      }
    />
  );
}
