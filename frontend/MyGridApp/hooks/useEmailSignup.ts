
import { useState } from 'react';

const API_URL = process.env.EXPO_PUBLIC_API_URL

export  function useEmailSignup () {

  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function emailSignup (username: string, email:string, password: string, locale: string) {

    const body = {
      username: username,
      email: email,
      password: password
    }

    const options = {
      method: "POST",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body)
    }

    try {
      setLoading(true);
      setError(null);

      const response = await fetch(`${API_URL}/auth/signup?language=${locale}`, options);

      if (response.status >= 500) {
        setError('AUTH');
        return false;
      }

      const data = await response.json();

      if (data.detail) {
        setError(data.detail);
        return false;
      }

      return data;

    } catch (e: any) {
      setError(e.message);
      return false;
    } finally {
      setLoading(false);
    }
  }

  return { emailSignup, error, loading };
}