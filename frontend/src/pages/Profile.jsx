// frontend/src/pages/Profile.jsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function Profile() {
  const [user, setUser] = useState({ name: '', email: '' });

  useEffect(() => {
    axios.get('/api/user/profile')
      .then(r => setUser(r.data.data))
      .catch(console.error);
  }, []);

  return (
    <div className="prose lg:prose-xl">
      <h1>Profile</h1>
      <p><strong>Name:</strong> {user.name}</p>
      <p><strong>Email:</strong> {user.email}</p>
      <button
        onClick={() => alert('Edit profile flow not implemented yet')}
        className="mt-4 bg-primary text-white px-4 py-2 rounded hover:bg-primary/90"
      >
        Edit Profile
      </button>
    </div>
  );
}
