import { useState } from "react";
import { apiFetch } from "../api";

export default function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleRegister = async () => {
    await apiFetch("/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, password })
    });

    alert("Registered! Please login.");
    window.location.href = "/login";
  };

  return (
    <div>
      <h2>Register</h2>
      <input placeholder="Email" onChange={e => setEmail(e.target.value)} />
      <input type="password" placeholder="Password" onChange={e => setPassword(e.target.value)} />
      <button onClick={handleRegister}>Register</button>
    </div>
  );
}