
import { useAuth } from '@/contexts/AuthContext';
import { useState } from 'react';

const API_URL = process.env.EXPO_PUBLIC_API_URL

export  function useLogout () {

  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const { accessToken } = useAuth();

  async function logout () {

    const options = {
      method: "POST",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`
      }
    }

    try {
      setLoading(true);
      setError(null);

      const response = await fetch(`${API_URL}/auth/logout`, options);

      if (!response.ok) {
        
        const data = await response.json()
        if (data.detail) {
          setError(data.detail);
          return false;
        }
      }

      return true;

    } catch (e: any) {
      setError(e.message);
      return false;
    } finally {
      setLoading(false);
    }
  }

  return { logout, error, loading };
}