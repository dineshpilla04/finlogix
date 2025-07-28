import * as React from 'react';
import { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext.tsx';

const Profile: React.FC = () => {
  const [profile, setProfile] = useState<any>(null);
  const [incomeType, setIncomeType] = useState('');
  const [defaultBudgetGoals, setDefaultBudgetGoals] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const { token } = useAuth();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await axios.get('/auth/profile', {
          headers: { Authorization: `Bearer ${token}` },
        });
        setProfile(response.data);
        setIncomeType(response.data.income_type || '');
        setDefaultBudgetGoals(JSON.stringify(response.data.default_budget_goals || {}, null, 2));
      } catch (error) {
        console.error('Error fetching profile:', error);
      }
    };
    fetchProfile();
  }, [token]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    let parsedBudgetGoals;
    try {
      parsedBudgetGoals = JSON.parse(defaultBudgetGoals);
    } catch (err) {
      setError('Default Budget Goals must be valid JSON');
      return;
    }
    try {
      await axios.put(
        '/auth/profile',
        {
          income_type: incomeType,
          default_budget_goals: parsedBudgetGoals,
        },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setSuccess('Profile updated successfully');
      setProfile((prev: any) => ({
        ...prev,
        income_type: incomeType,
        default_budget_goals: parsedBudgetGoals,
      }));
    } catch (error) {
      setError('Failed to update profile');
    }
  };

  if (!profile) {
    return <div>Loading...</div>;
  }

  return (
    <div className="max-w-md mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">Profile</h2>
      <p><strong>Username:</strong> {profile.username}</p>
      <p><strong>Email:</strong> {profile.email}</p>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block font-semibold mb-1" htmlFor="incomeType">Income Type</label>
          <input
            id="incomeType"
            type="text"
            value={incomeType}
            onChange={(e) => setIncomeType(e.target.value)}
            className="border p-2 w-full"
          />
        </div>
        <div className="mb-4">
          <label className="block font-semibold mb-1" htmlFor="defaultBudgetGoals">Default Budget Goals (JSON)</label>
          <textarea
            id="defaultBudgetGoals"
            value={defaultBudgetGoals}
            onChange={(e) => setDefaultBudgetGoals(e.target.value)}
            className="border p-2 w-full h-32 font-mono"
          />
        </div>
        {error && <p className="text-red-600 mb-2">{error}</p>}
        {success && <p className="text-green-600 mb-2">{success}</p>}
        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Update Profile
        </button>
      </form>
    </div>
  );
};

export default Profile;
