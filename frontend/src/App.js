import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginForm from './components/LoginForm';
import FolderContent from './components/FolderContent';
import AdminPage from './components/AdminPage';
import 'bootstrap/dist/css/bootstrap.min.css';


const App = () => {
  const [loggedIn, setLoggedIn] = useState(false);
  const [initialPath, setInitialPath] = useState('/folder'); // Assurez-vous que ce chemin est correct

  const handleLogin = (path) => {
    setLoggedIn(true);
    setInitialPath(path || '/folder'); // Assurez-vous que `path` a une valeur correcte
  };

  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={!loggedIn ? <LoginForm onLogin={handleLogin} /> : <Navigate to={initialPath} replace />}
        />
        <Route path="/admin" element={<AdminPage />} />
        <Route path="/folder" element={<FolderContent />} />
      </Routes>
    </Router>
  );
};

export default App;
