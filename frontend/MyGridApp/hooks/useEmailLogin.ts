
import { useState } from 'react';

const API_URL = process.env.EXPO_PUBLIC_API_URL

export  function useEmailLogin () {

  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  async function emailLogin (username: string, password: string, locale: string) {

    const body = `${encodeURIComponent('username')}=${encodeURIComponent(username)}&${encodeURIComponent('password')}=${encodeURIComponent(password)}`

    const options = {
      method: "POST",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: body
    }

    try {
      setLoading(true);
      setError(null);

      const response = await fetch(`${API_URL}/auth/login-email?language=${locale}`, options);
      const data = await response.json()

      if (data.detail) {
        setError(data.detail);
        return false;
      }

      console.log(data)

      return {
        user: data.user,
        accessToken: data.access_token.access_token,
        refreshToken: data.refresh_token.refresh_token
      };

    } catch (e: any) {
      setError(e.message);
      return false;
    } finally {
      setLoading(false);
    }
  }

  return { emailLogin, error, loading };
}