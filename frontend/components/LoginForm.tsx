"use client";

import { useState } from "react";
import { apiPost } from "@/lib/api";

type Props = {
  onSwitch: () => void;
};

export default function LoginForm({ onSwitch }: Props) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const data = await apiPost<{ access_token: string }>(
        "/auth/login",
        { email, password }
      );
      localStorage.setItem("access_token", data.access_token);
      window.location.href = "/chat";
    } catch {
      setError("Invalid email or password");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleLogin} className="w-full space-y-4">
      <h2 className="text-2xl font-semibold text-center">Login</h2>

      {error && <p className="text-red-500 text-sm">{error}</p>}

      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className="
          w-full px-3 py-2.5
          border border-neutral-300
          rounded-md
          focus:outline-none
          focus:ring-2 focus:ring-neutral-800
        "
      />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        className="
          w-full px-3 py-2.5
          border border-neutral-300
          rounded-md
          focus:outline-none
          focus:ring-2 focus:ring-neutral-800
        "
      />

      <button
        disabled={loading}
        className="
          w-full py-2.5
          bg-neutral-900 text-white
          rounded-md text-sm font-medium
          hover:bg-neutral-800 transition
        "
      >
        {loading ? "Logging in..." : "Login"}
      </button>

      <p className="text-sm text-center text-neutral-500">
        Don’t have an account?{" "}
        <button
          type="button"
          onClick={onSwitch}
          className="underline"
        >
          Sign up
        </button>
      </p>
    </form>
  );
}
