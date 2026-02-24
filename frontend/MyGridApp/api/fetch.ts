import { AuthContextType } from "@/contexts/AuthContext";
import { refreshLogin } from "./refresh";

const API_URL = process.env.EXPO_PUBLIC_API_URL

export async function apiFetch(
  endpoint: string,
  body: any,
  auth: AuthContextType
) {
  
  const accessToken = auth.accessToken;

  async function request (token: string | null) {

    const options = {
      method: "POST",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body)
    }
    
    return fetch(`${API_URL}${endpoint}`, options)
  }

  let response = await request(accessToken)

  if (response.status === 401) {
    try {
      const refreshDatas = await refreshLogin(accessToken, auth.refreshToken);
      auth.login(refreshDatas)
      response = await request(refreshDatas.access_token.access.token)
    } catch (e) {
      await auth.logout()
      throw e
    }
  }

  if (!response.ok) {
    throw new Error("API request failed")
  }

  return response
}