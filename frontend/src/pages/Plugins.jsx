// frontend/src/pages/Plugins.jsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function Plugins() {
  const [local, setLocal] = useState([]);
  const [installed, setInstalled] = useState([]);
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  // Load lists on mount
  useEffect(() => {
    axios.get('/api/plugins/list')
      .then(r => {
        setLocal(r.data.data.local);
        setInstalled(r.data.data.installed);
      })
      .catch(console.error);
  }, []);

  const search = () => {
    axios.get(`/api/plugins/search?q=${encodeURIComponent(query)}`)
      .then(r => setResults(r.data.data))
      .catch(console.error);
  };

  const install = (name) => {
    axios.post('/api/plugins/install', { name })
      .then(() => {
        // refresh lists
        return axios.get('/api/plugins/list');
      })
      .then(r => {
        setLocal(r.data.data.local);
        setInstalled(r.data.data.installed);
        setResults([]);
      })
      .catch(console.error);
  };

  return (
    <div className="prose lg:prose-xl space-y-4">
      <h1>Plugins</h1>

      <div className="flex space-x-2">
        <input
          type="text"
          placeholder="Search plugins..."
          value={query}
          onChange={e => setQuery(e.target.value)}
          className="border rounded p-1 flex-grow"
        />
        <button
          onClick={search}
          className="bg-secondary text-white px-3 rounded hover:bg-secondary/90"
        >
          Search
        </button>
      </div>

      {results.length > 0 && (
        <div>
          <h2>Search Results</h2>
          <ul className="list-disc pl-6 space-y-1">
            {results.map(r => (
              <li key={r}>
                {r}{' '}
                <button
                  onClick={() => install(r)}
                  className="text-primary hover:underline"
                >
                  Install
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}

      <h2>Local Plugins</h2>
      <ul className="list-disc pl-6">
        {local.map(p => <li key={p}>{p}</li>)}
      </ul>

      <h2>Installed Packages</h2>
      <ul className="list-disc pl-6">
        {installed.map(i => <li key={i}>{i}</li>)}
      </ul>
    </div>
  );
}
