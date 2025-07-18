import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext.tsx';
import Login from './components/Login.tsx';
import Register from './components/Register.tsx';
import Dashboard from './components/Dashboard.tsx';
import Transactions from './components/Transactions.tsx';
import Profile from './components/Profile.tsx';
import AdminPanel from './components/AdminPanel.tsx';
import PromoteUser from './components/PromoteUser.tsx';
import ChatBox from './components/ChatBox.tsx';

const App: React.FC = () => {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/transactions" element={<Transactions />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/admin" element={<AdminPanel />} />
          <Route path="/promote-user" element={<PromoteUser />} />
          <Route path="/chat" element={<ChatBox />} />
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
};

export default App;
