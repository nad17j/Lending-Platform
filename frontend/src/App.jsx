import React from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import LoginCard from './components/LoginCard';
import UnderwriterView from './components/UnderwriterView';

function AppContent() {
  const { isAuthenticated } = useAuth();
  
  // If user is not authenticated with a JWT token, force render the login wall
  if (!isAuthenticated) {
    return <LoginCard />;
  }
  
  // Otherwise, render the internal bank workbench console
  return <UnderwriterView />;
}

export default function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}