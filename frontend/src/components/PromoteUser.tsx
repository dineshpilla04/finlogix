import * as React from 'react';
import { useState } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext.tsx';

const PromoteUser: React.FC = () => {
  const [userId, setUserId] = useState('');
  const [message, setMessage] = useState('');
  const { token } = useAuth();

  const handlePromote = async () => {
    if (!userId) {
      setMessage('Please enter a user ID');
      return;
    }
    try {
      const response = await axios.post(
        `http://localhost:5000/admin/users/${userId}/promote`,
        {},
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setMessage(response.data.msg);
    } catch (error: any) {
      if (error.response) {
        setMessage(error.response.data.msg || 'Error promoting user');
      } else {
        setMessage('Error promoting user');
      }
    }
  };

  return (
    <div className="max-w-md mx-auto p-4 border rounded shadow">
      <h2 className="text-2xl font-bold mb-4">Promote User to Admin</h2>
      <input
        type="text"
        placeholder="Enter User ID"
        value={userId}
        onChange={(e) => setUserId(e.target.value)}
        className="border p-2 w-full mb-4"
      />
      <button
        onClick={handlePromote}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Promote
      </button>
      {message && <p className="mt-4 text-red-600">{message}</p>}
    </div>
  );
};

export default PromoteUser;
