import * as React from 'react';
import { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext.tsx';

const Profile: React.FC = () => {
  const [profile, setProfile] = useState<any>(null);
  const { token } = useAuth();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await axios.get('/auth/profile', {
          headers: { Authorization: `Bearer ${token}` },
        });
        setProfile(response.data);
      } catch (error) {
        console.error('Error fetching profile:', error);
      }
    };
    fetchProfile();
  }, [token]);

  if (!profile) {
    return <div>Loading...</div>;
  }

  return (
    <div className="max-w-md mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">Profile</h2>
      <p><strong>Username:</strong> {profile.username}</p>
      <p><strong>Email:</strong> {profile.email}</p>
      <p><strong>Income Type:</strong> {profile.income_type}</p>
      <p><strong>Default Budget Goals:</strong> {JSON.stringify(profile.default_budget_goals)}</p>
    </div>
  );
};

export default Profile;
