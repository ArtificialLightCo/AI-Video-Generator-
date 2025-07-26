// frontend/src/pages/Projects.jsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function Projects() {
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    axios.get('/api/projects/list')
      .then(r => setProjects(r.data.data))
      .catch(console.error);
  }, []);

  return (
    <div className="prose lg:prose-xl">
      <h1>Projects</h1>
      <ul className="list-disc pl-6">
        {projects.map(p => (
          <li key={p}>{p}</li>
        ))}
      </ul>
    </div>
  );
}
