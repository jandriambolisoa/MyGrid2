import * as Localization from 'expo-localization';
import * as SecureStore from 'expo-secure-store';

const API_URL = process.env.EXPO_PUBLIC_API_URL
const locale = Localization.getLocales()[0]?.languageCode || 'en';

export async function registerPushToken (accessToken: string | null, pushToken: string) {

  if (!accessToken || !pushToken) {
    throw new Error('Missing token');
  }

  const body = {
    token: pushToken,
    language: locale
  }

  const options = {
    method: "POST",
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${accessToken}`
    },
    body: JSON.stringify(body)
  }

  const response = await fetch(`${API_URL}/notifications/push`, options);

  if (!response.ok) {
    throw new Error('Push token failed');
  }

  const data = await response.json();

  if (data?.detail) {
    throw new Error(data.detail);
  }

  await SecureStore.setItemAsync('pushToken', pushToken);

  return data;
}