import { useState } from "react";

export function useApi<T = any> (initLoading = false) {

  const [datas, setDatas] = useState<T | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(initLoading);
  const [status, setStatus] = useState<number | null>(null);

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

  async function api ({ endpoint, body, method = 'GET'} : { endpoint: string, body?: unknown, method?: 'GET' | 'POST' | 'PUT' | 'DELETE' }) {

    setLoading(true);
    setError(null);

    try {

      const response = await fetch(endpoint, {
        method,
        ...(body ? { body: JSON.stringify(body) } : {})
      });

      setStatus(response.status);

      if (response.status >= 500) {
        setError('Server error');
        return false;
      }

      const data = await response.json();

      if (!response.ok) {
        setError(data?.detail?.message ?? data?.detail ?? data.error ?? 'An error occurred');
        return false;
      }

      setDatas(data);
      return true;

    } catch (e) {
      setError(e instanceof Error ? e.message : 'An error occurred');
      return false
    } finally {
      setLoading(false)
    }
  }

  return { datas, error, status, loading, api }
}