
import { useState } from 'react';
import * as Localization from 'expo-localization'

const API_URL = process.env.EXPO_PUBLIC_API_URL
const locale = Localization.getLocales()[0]?.languageCode || 'en';

export function useEmailLogin () {

  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function emailLogin (username: string, password: string) {

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

      if (response.status >= 500) {
        setError('AUTH');
        return false;
      }

      const data = await response.json()

      if (data.detail) {
        setError(data.detail);
        return false;
      }

      return data

    } catch (e: any) {
      setError(e.message);
      return false;
    } finally {
      setLoading(false);
    }
  }

  return { emailLogin, error, loading };
}