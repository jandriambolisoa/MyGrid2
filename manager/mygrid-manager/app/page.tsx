"use client"

import { useState, useEffect } from "react";
import { useEmailLogin } from "@/hooks"

export default function Home () {

  const { emailLogin, error, loading } = useEmailLogin();

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  useEffect(() => {
    if (error) {
      setErrorMsg(error);
    }
  }, [error])

  async function handleLogin () {

    setErrorMsg('');

    if (username.length === 0 || password.length === 0) {
      setErrorMsg('Missing information');
      return;
    }

    const res = await emailLogin(username, password);
    if (res.success) {
      console.log("Login ok!")
    }

  }

  return (
    <div className="container">
      <h1 className="title">Login</h1>
      <input
        className="input"
        placeholder="Email or username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        className="input"
        style={{ marginBottom: 44 }}
        placeholder="Password"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button className="button" onClick={handleLogin}>Login</button>
      <h1 className="error">{errorMsg}</h1>
    </div>
  )
}