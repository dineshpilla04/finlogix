import * as React from 'react';
import { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext.tsx';

const AdminPanel: React.FC = () => {
  const [categories, setCategories] = useState<string[]>([]);
  const [users, setUsers] = useState<any[]>([]);
  const { token } = useAuth();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const categoriesResponse = await axios.get('/admin/categories', {
          headers: { Authorization: `Bearer ${token}` },
        });
        setCategories(categoriesResponse.data);

        const usersResponse = await axios.get('/admin/users', {
          headers: { Authorization: `Bearer ${token}` },
        });
        setUsers(usersResponse.data);
      } catch (error) {
        console.error('Error fetching admin data:', error);
      }
    };
    fetchData();
  }, [token]);

  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-4">Admin Panel</h2>
      <div className="mb-4">
        <h3 className="text-xl font-semibold">Categories</h3>
        <ul>
          {categories.map((cat) => (
            <li key={cat}>{cat}</li>
          ))}
        </ul>
      </div>
      <div>
        <h3 className="text-xl font-semibold">Users</h3>
        <ul>
          {users.map((user) => (
            <li key={user.id}>{user.username} - {user.email}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default AdminPanel;
