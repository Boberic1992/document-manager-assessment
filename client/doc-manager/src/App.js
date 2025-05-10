import './App.css';
import FileVersions from './FileVersions'
import FileUpload from './FileUpload'
import Login from './Login';
import React, { useState } from 'react'


function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [refresh, setRefresh] = useState(0);

  const handleLogin = (newToken) => {
    setToken(newToken);
    localStorage.setItem('token', newToken);
  };

  const handleLogout = () => {
    setToken(null);
    localStorage.removeItem('token');
  };

  const handleUpload = () => setRefresh(r => r + 1)

  return (
    <div className="App">
      {token && (
        <div className="logout-container">
          <button onClick={handleLogout}>Logout</button>
        </div>
      )}
      <header className="App-header">
        {!token ? (
          <Login onLogin={handleLogin} />
        ) : (
          <>
            <FileUpload token={token} onUpload={handleUpload} />
            <FileVersions token={token} key={refresh} />
          </>
        )}
      </header>
    </div>
  );
}

export default App;
