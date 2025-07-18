import * as React from 'react';
import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Register: React.FC = () => {
  const [form, setForm] = useState({
    username: '',
    email: '',
    password: '',
  });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      await axios.post('/auth/register', form);
      navigate('/login');
    } catch (err: any) {
      setError(err.response?.data?.msg || 'Registration failed');
    }
  };

  return (
    <div className="max-w-md mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">Register</h2>
      {error && <div className="text-red-600 mb-2">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div className="mb-2">
          <label className="block mb-1">Username</label>
          <input
            type="text"
            name="username"
            value={form.username}
            onChange={handleChange}
            required
            className="border p-2 w-full"
          />
        </div>
        <div className="mb-2">
          <label className="block mb-1">Email</label>
          <input
            type="email"
            name="email"
            value={form.email}
            onChange={handleChange}
            required
            className="border p-2 w-full"
          />
        </div>
        <div className="mb-2">
          <label className="block mb-1">Password</label>
          <input
            type="password"
            name="password"
            value={form.password}
            onChange={handleChange}
            required
            className="border p-2 w-full"
          />
        </div>
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
          Register
        </button>
      </form>
    </div>
  );
};

export default Register;
