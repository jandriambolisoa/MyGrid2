import { apiFetch, FetchProps } from "@/api/fetch";
import { useToast } from "@/contexts/ToastContext";
import { scopedI18n } from "@/translations/i18n";
import { useRouter } from "expo-router";
import { useState } from "react";

export function useApi<T = any> (initLoading = false, toast = true) {

  const t = scopedI18n('hooks.useApi');
  const router = useRouter();

  const { showToast } = useToast();

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

  async function api (props: FetchProps) {

    setLoading(true)
    setError(null)

    try {

      const response = await apiFetch(props);

      setStatus(response.status);

      if (response.status >= 500) {
        setError('Server error');
        if (toast) {
          showToast({
            title: 'Server error',
            type: 'error'
          })
        }
        return false;
      }

      const data = await response.json();

      if (response.status === 428) {
        router.replace('/profile/modify/resetPassword');
      }

      if (!response.ok) {
        setError(data?.detail?.message ?? data?.detail ?? t('anError'))
        if (toast) {
          showToast({
            title: data?.detail?.message ?? data?.detail ?? t('anError'),
            type: 'error'
          })
        }
        return false;
      }

      setDatas(data);
      return true;

    } catch (e) {
      setError(e instanceof Error ? e.message : t('anError'));
      if (toast) {
        showToast({
          title: e instanceof Error ? e.message : t('anError'),
          type: 'error'
        })
      }
      return false
    } finally {
      setLoading(false)
    }
  }

  return { datas, error, status, loading, api }
}