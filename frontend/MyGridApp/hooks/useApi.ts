import { apiFetch, FetchProps } from "@/api/fetch";
import { useState } from "react";

export function useApi<T = any> (initLoading = false) {

  const [datas, setDatas] = useState<T | null>(null);
  const [error, setError] = useState<unknown>(null);
  const [loading, setLoading] = useState(initLoading);

  /**
   * Makes an API call using `apiFetch` and updates state.
   *
   * @param {FetchProps} props - Object containing request info:
   * @param {string} props.endpoint - API endpoint (e.g., '/users').
   * @param {unknown} [props.body] - Optional request body for POST/PUT requests.
   * @param {'GET' | 'POST' | 'PUT' | 'DELETE'} props.method - HTTP method.
   * @param {string} props.contentType - Headers Content-Type.
   * @param {AuthContextType} props.auth - Authentication context with tokens and login/logout methods.
   *
   * @returns {Promise<T | undefined>} - Resolves with API response data of type T, or undefined if there is an error.
   */

  async function api (props: FetchProps) {

    setLoading(true)
    setError(null)

    try {
      const data = await apiFetch<T>(props);
      setDatas(data);
      return true;
    } catch (e) {
      setError(e)
      return false
    } finally {
      setLoading(false)
    }
  }

  return { datas, error, loading, api }
}