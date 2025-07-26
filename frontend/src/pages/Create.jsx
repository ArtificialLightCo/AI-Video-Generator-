// frontend/src/pages/Create.jsx
import React, { useState } from 'react';
import axios from 'axios';
import { toast } from 'react-toastify';

export default function Create() {
  const [prompt, setPrompt] = useState('');
  const [duration, setDuration] = useState(10);
  const [initImage, setInitImage] = useState(null);
  const [sttFile, setSttFile] = useState(null);
  const [jobId, setJobId] = useState(null);
  const [status, setStatus] = useState(null);
  const [refine, setRefine] = useState(false);

  const start = async () => {
    const form = new FormData();
    if (initImage) form.append('init_image', initImage);
    if (sttFile) form.append('stt_audio', sttFile);
    form.append('prompt', prompt);
    form.append('duration', duration);
    form.append('assist', refine);
    toast.info('Starting generation...');
    const res = await axios.post('/api/generate', form, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    const jid = res.data.data.job_id;
    setJobId(jid);
    setStatus('queued');
    poll(jid);
  };

  const poll = async (id) => {
    const r = await axios.get(`/api/status/${id}`);
    const s = r.data.data.status;
    setStatus(s);
    if (s === 'done') toast.success('Generation complete!');
    else if (s === 'error') toast.error('Error during generation');
    else setTimeout(() => poll(id), 2000);
  };

  return (
    <div className="prose lg:prose-xl">
      <h1>Create Video</h1>
      <div className="space-y-4">
        <label>Prompt (use “|” to split scenes)</label>
        <textarea
          className="w-full border rounded p-2"
          rows={3}
          value={prompt}
          onChange={e => setPrompt(e.target.value)}
        />
        <div className="flex space-x-4">
          <div>
            <label>Duration (s)</label>
            <input
              type="number"
              className="w-20 border rounded p-1"
              value={duration}
              onChange={e => setDuration(+e.target.value)}
            />
          </div>
          <div>
            <label>Init Image</label>
            <input
              type="file"
              accept="image/*"
              onChange={e => setInitImage(e.target.files[0])}
            />
          </div>
          <div>
            <label>STT Audio</label>
            <input
              type="file"
              accept="audio/*"
              onChange={e => setSttFile(e.target.files[0])}
            />
          </div>
        </div>
        <div className="flex items-center space-x-4">
          <label className="flex items-center">
            <input
              type="checkbox"
              className="mr-2"
              checked={refine}
              onChange={e => setRefine(e.target.checked)}
            />
            Refine Prompt
          </label>
          <button
            onClick={start}
            className="bg-primary text-white px-4 py-2 rounded hover:bg-primary/90"
          >
            Generate
          </button>
        </div>
        {jobId && <p>Job {jobId}: {status}</p>}
        {status === 'done' && (
          <div className="mt-4">
            <video
              src={`/outputs/final_${jobId}.mp4`}
              controls
              className="w-full rounded shadow"
            />
          </div>
        )}
      </div>
    </div>
);
}
