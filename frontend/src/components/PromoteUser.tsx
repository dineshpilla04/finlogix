import * as React from 'react';
import { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext.tsx';

const PromoteUser: React.FC = () => {
  const [userId, setUserId] = useState('');
  const [message, setMessage] = useState('');
  const [users, setUsers] = useState<any[]>([]);
  const { token } = useAuth();

  const handlePromote = async () => {
    if (!userId) {
      setMessage('Please enter a user ID');
      return;
    }
    try {
      const response = await axios.post(
        `/admin/users/${userId}/promote`,
        {},
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setMessage(response.data.msg);
      fetchUsers(); // Refresh user list after promotion
    } catch (error: any) {
      if (error.response) {
        setMessage(error.response.data.msg || 'Error promoting user');
      } else {
        setMessage('Error promoting user');
      }
    }
  };

  const fetchUsers = async () => {
    try {
      const response = await axios.get('/admin/users', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setUsers(response.data);
    } catch (error) {
      setMessage('Error fetching users');
    }
  };

  useEffect(() => {
    fetchUsers();
  }, [token]);

  return (
    <div className="max-w-4xl mx-auto p-4 border rounded shadow">
      <h2 className="text-2xl font-bold mb-4">Promote User to Admin</h2>
      <div className="mb-4">
        <input
          type="text"
          placeholder="Enter User ID"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          className="border p-2 w-full mb-2"
        />
        <button
          onClick={handlePromote}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Promote
        </button>
        {message && <p className="mt-4 text-red-600">{message}</p>}
      </div>
      <h3 className="text-xl font-semibold mb-2">All Users</h3>
      {users.length === 0 ? (
        <p>No users found.</p>
      ) : (
        <table className="w-full border-collapse border border-gray-300">
          <thead>
            <tr>
              <th className="border border-gray-300 px-2 py-1">ID</th>
              <th className="border border-gray-300 px-2 py-1">Username</th>
              <th className="border border-gray-300 px-2 py-1">Email</th>
              <th className="border border-gray-300 px-2 py-1">Income Type</th>
              <th className="border border-gray-300 px-2 py-1">Default Budget Goals</th>
              <th className="border border-gray-300 px-2 py-1">Admin</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr key={user.id}>
                <td className="border border-gray-300 px-2 py-1">{user.id}</td>
                <td className="border border-gray-300 px-2 py-1">{user.username}</td>
                <td className="border border-gray-300 px-2 py-1">{user.email}</td>
                <td className="border border-gray-300 px-2 py-1">{user.income_type || '-'}</td>
                <td className="border border-gray-300 px-2 py-1">
                  <pre className="whitespace-pre-wrap">{JSON.stringify(user.default_budget_goals, null, 2)}</pre>
                </td>
                <td className="border border-gray-300 px-2 py-1">{user.is_admin ? 'Yes' : 'No'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default PromoteUser;
