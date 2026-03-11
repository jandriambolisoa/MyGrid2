import * as Localization from 'expo-localization'

const API_URL = process.env.EXPO_PUBLIC_API_URL
const locale = Localization.getLocales()[0]?.languageCode || 'en';

export async function refreshLogin (accessToken: string | null, refreshToken: string | null) {

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

  const response = await fetch(`${API_URL}/auth/login-refresh-token?language=${locale}`, options);

  if (response.status >= 500) {
    throw new Error('SERVER');
  }

  if (response.status === 401) {
    throw new Error('AUTH');
  }

  if (!response.ok) {
    throw new Error('UNKOWN');
  }

  const data = await response.json();

  return data;
}