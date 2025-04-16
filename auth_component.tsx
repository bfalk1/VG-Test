import React, { useState } from 'react';
import axios from 'axios';

export default function AuthComponent() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [token, setToken] = useState<string | null>(null);
  const [role, setRole] = useState<string | null>(null);
  const [dashboard, setDashboard] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const login = async () => {
    try {
      const res = await axios.post('http://localhost:3001/login', { email, password });
      setToken(res.data.token);
      setRole(res.data.role);
      setError(null);
    } catch (err) {
      setError("Login failed. Check your credentials.");
    }
  };

  const fetchDashboard = async () => {
    try {
      const res = await axios.get('http://localhost:3001/dashboard', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setDashboard(res.data.message);
      setError(null);
    } catch (err) {
      setError("Failed to load dashboard.");
    }
  };

  return (
    <div className="p-4">
      <h2>Login</h2>
      <input placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
      <input placeholder="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} />
      <button onClick={login}>Login</button>

      {role && (
        <>
          <p>Logged in as: {role}</p>
          <button onClick={fetchDashboard}>Load Dashboard</button>
        </>
      )}

      {dashboard && <p>{dashboard}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
}