import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export default function Telemetry() {
  const [data, setData] = useState({ labels: [], datasets: [] });

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const res = await axios.get('/api/metrics');
        const stats = res.data.data;
        setData(prev => {
          const time = new Date().toLocaleTimeString();
          return {
            labels: [...prev.labels.slice(-9), time],
            datasets: [
              {
                label: 'CPU %',
                data: [...(prev.datasets[0]?.data || []).slice(-9), stats.cpu],
                borderColor: 'rgba(75, 192, 192, 1)',
                fill: false
              },
              {
                label: 'RAM %',
                data: [...(prev.datasets[1]?.data || []).slice(-9), stats.memory.percent],
                borderColor: 'rgba(153, 102, 255, 1)',
                fill: false
              }
            ]
          };
        });
      } catch (e) {
        console.error('Failed to fetch metrics:', e);
      }
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-2 bg-white shadow-inner">
      <Line data={data} />
    </div>
  );
}
