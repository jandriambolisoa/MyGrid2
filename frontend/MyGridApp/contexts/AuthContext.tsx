import { createContext, useContext, useState } from "react";

export const AuthContext = createContext(undefined);

export function AuthProvider ({ children }: any) {
  const [user, setUser] = useState(null);

  async function login (token: string) {

  }

  async function logout () {
    
  }

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
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

