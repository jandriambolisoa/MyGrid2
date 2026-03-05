import { AuthContextType } from "@/contexts/AuthContext";
import { refreshLogin } from "./refresh";

const API_URL = process.env.EXPO_PUBLIC_API_URL

export type ApiError = {
  detail: string;
}

export type FetchProps = {
  endpoint: string;
  body?: unknown;
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
  contentType?: string;
  auth: AuthContextType;
}

export async function apiFetch ({
  endpoint,
  body,
  method='GET',
  contentType='application/json',
  auth
}: FetchProps): Promise<any> {
  
  const accessToken = auth.accessToken;

  async function request (token: string | null) {

  const options: RequestInit = {
    method: method,
    headers: {
      "Accept": "application/json",
      "Content-Type": contentType,
      ...(token && { Authorization: `Bearer ${token}` }),
    }
  };
  
  if (body !== undefined) {
    if (body instanceof FormData) {
      options.body = body
    } else {
      options.body = JSON.stringify(body)
    }
  }
    
    return fetch(`${API_URL}${endpoint}`, options)
  }

  let response = await request(accessToken)

  if (response.status === 401) {
    try {
      const refreshDatas = await refreshLogin(accessToken, auth.refreshToken);
      await auth.login(refreshDatas);
      response = await request(refreshDatas.access_token.access.token);
    } catch (e) {
      await auth.logout()
      throw e
    }
  }

  return response
}