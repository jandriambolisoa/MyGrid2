import { createContext, useContext, useState } from "react";

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export type AuthData = {
  user: any;
  accessToken: string;
  refreshToken: string;
}

export type AuthContextType = {
  user: any;
  accessToken: string | null;
  refreshToken: string | null;
  login: (authData: AuthData) => void;
  logout: () => void;
  isAuthenticated: boolean;
}

export function AuthProvider ({ children }: any) {

  const [user, setUser] = useState(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [refreshToken, setRefreshToken] = useState<string | null>(null);

  async function login (authData: AuthData) {
    setUser(authData.user);
    setAccessToken(authData.accessToken);
    setRefreshToken(authData.refreshToken);

    // Store tokens in secure storage or AsyncStorage here
  }

  async function logout () {
    setUser(null);
    setAccessToken(null);
    setRefreshToken(null);

    // Clear tokens from storage here
  }

  return (
    <AuthContext.Provider value={{
      user,
      accessToken,
      refreshToken,
      login,
      logout,
      isAuthenticated: !!user
      }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth () {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

