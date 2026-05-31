import React, { createContext, useState, useContext } from 'react';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(null);
  const [user, setUser] = useState(null);

  const loginUser = (dummyJwtToken) => {
    // In production, we decode the payload segment of the JWT to extract officer name and roles
    setToken(dummyJwtToken);
    setUser({
      name: "Officer Gamage",
      role: "UNDERWRITER_LEVEL_2",
      branch: "Colombo Central Core"
    });
  };

  const logoutUser = () => {
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ token, user, loginUser, logoutUser, isAuthenticated: !!token }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);