
import { useState } from 'react';
import * as Localization from 'expo-localization'
import * as SecureStore from 'expo-secure-store'

const API_URL = process.env.EXPO_PUBLIC_API_URL
const locale = Localization.getLocales()[0]?.languageCode || 'en';

export function useRefreshLogin () {

  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  async function refreshLogin () {

    const accessToken = await SecureStore.getItemAsync('accessToken')
    const refreshToken = await SecureStore.getItemAsync('refreshToken')

    if (!accessToken || !refreshToken) {
      throw new Error('Missing token')
    }

    const body = {
      access_token: {
        access_token: accessToken,
        token_type: "bearer"
      },
      refresh_token: {
        refresh_token: refreshToken,
        token_type: "bearer"
      }
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

      const response = await fetch(`${API_URL}/auth/login-refresh-token?language=${locale}`, options);
      const data = await response.json()

      if (data.detail) {
        setError(data.detail);
        return false;
      }

      // Add the user in the return

      return {
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

  return { refreshLogin, error, loading };
}