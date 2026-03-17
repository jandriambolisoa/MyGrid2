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

      let data: any;
      const text = await response.text();
      try {
        data = JSON.parse(text);
      } catch {
        data = { message: text };
      }

      if (response.status >= 500) {
        setError('SERVER');
        return false;
      }

      if (!response.ok) {
        console.log(data)
        setError(data?.detail || data?.message || data?.error || `HTTP ${response.status}`);
        return false;
      }

      // Erreur renvoyée dans le JSON
      if (data?.detail) {
        setError(data.detail);
        return false;
      }

      return data

    } catch (e: any) {
      setError(e?.message || "An unexpected error occured.");
      return false;
    } finally {
      setLoading(false);
    }
  }

  return { emailLogin, error, loading };
}