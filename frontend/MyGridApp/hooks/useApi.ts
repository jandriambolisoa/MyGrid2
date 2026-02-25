import { apiFetch, FetchProps } from "@/api/fetch";
import { useState } from "react";

export function useApi<T = any> () {

  const [datas, setDatas] = useState<T | null>(null);
  const [error, setError] = useState<unknown>(null);
  const [loading, setLoading] = useState(false);

  async function api (props: FetchProps) {

    setLoading(true)
    setError(null)

    try {
      const data = await apiFetch<T>(props);
      setDatas(data);
      return data;
    } catch (e) {
      setError(e)
    } finally {
      setLoading(false)
    }
  }

  return { datas, error, loading, api }
}