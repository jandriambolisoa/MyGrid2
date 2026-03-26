const API_URL = process.env.EXPO_PUBLIC_API_URL

export async function forgotPassword (email: string | null) {

  if (!email) {
    throw new Error('Missing email');
  }

  const options = {
    method: "GET",
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
  }

  const response = await fetch(`${API_URL}/auth/forgot-password?credential=${email}`, options);

  if (!response.ok) {
    return false;
  }

  return true;
}