"use client"

import { useState } from "react";

export function useEmailLogin () {

  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function emailLogin (username: string, password: string) {

    try {
      setLoading(true);
      setError(null);

      const response = await fetch("/api/login", {
        method: 'POST',
        body: JSON.stringify({ username, password }),
        headers: { "Content-Type": "application/json"}
      });

      if (response.status >= 500) {
        setError('SERVER');
        return false;
      }

      const data = await response.json()

      if (data.detail) {
        setError(data.detail);
        return false;
      }

      return data

    } catch (e: any) {
      setError(String(e.message));
      return false;
    } finally {
      setLoading(false);
    }
  }

  return { emailLogin, error, loading };
}