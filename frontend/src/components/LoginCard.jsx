import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';

export default function LoginCard() {
  const { loginUser } = useAuth();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (username && password) {
      // Simulating receiving a secure signed token back from our OAuth keycloak cluster
      const mockSignedJWT = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6Ik9mZmljZXIgR2FtYWdlIiwicm9sZXMiOlsiVU5ERVJXUklURVJfTEVWRUxfMiJdfQ.signature";
      loginUser(mockSignedJWT);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-50 px-4 py-12 sm:px-6 lg:px-8">
      <div className="w-full max-w-md space-y-8 rounded-2xl bg-white p-8 shadow-xl border border-slate-100">
        <div>
          <div className="mx-auto h-12 w-12 rounded-xl bg-slate-900 flex items-center justify-center text-white text-xl font-bold">🇱🇰</div>
          <h2 className="mt-6 text-center text-3xl font-bold tracking-tight text-slate-900">Sri Lanka Lending Core</h2>
          <p className="mt-2 text-center text-sm text-slate-600">Secure Employee Gateway Terminal</p>
        </div>
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="space-y-4 rounded-md">
            <div>
              <label className="text-xs font-semibold text-slate-700 uppercase tracking-wider">Corporate ID Email</label>
              <input type="text" required value={username} onChange={e => setUsername(e.target.value)} 
                className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 placeholder-slate-400 focus:border-slate-900 focus:outline-none sm:text-sm" placeholder="officer.g@bank.lk" />
            </div>
            <div>
              <label className="text-xs font-semibold text-slate-700 uppercase tracking-wider">Passphrase Key</label>
              <input type="password" required value={password} onChange={e => setPassword(e.target.value)} 
                className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 placeholder-slate-400 focus:border-slate-900 focus:outline-none sm:text-sm" placeholder="••••••••" />
            </div>
          </div>
          <button type="submit" className="group relative flex w-full justify-center rounded-lg bg-slate-900 px-3 py-2.5 text-sm font-semibold text-white transition hover:bg-slate-800 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2">
            Verify Identity & Log In
          </button>
        </form>
      </div>
    </div>
  );
}