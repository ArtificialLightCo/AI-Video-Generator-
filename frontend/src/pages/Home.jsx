import React from 'react';
import TemplateCard from '../components/TemplateCard';
import { Carousel } from 'react-responsive-carousel';
import 'react-responsive-carousel/lib/styles/carousel.min.css';

const templates = [
  { id: 'text2video', title: 'Text to Video', icon: '📝' },
  { id: 'superhero', title: 'Superhero Effect', icon: '🦸' },
  { id: 'dance', title: 'Dance Animation', icon: '💃' },
  { id: 'hug', title: 'AI Hug', icon: '🤗' },
];

const banners = [
  '/static/banner1.jpg',
  '/static/banner2.jpg',
  '/static/banner3.jpg'
];

export default function Home() {
  return (
    <div className="space-y-6">
      <Carousel autoPlay infiniteLoop showThumbs={false} showStatus={false} className="rounded-lg">
        {banners.map((src, idx) => (
          <div key={idx}>
            <img src={src} alt={`Banner ${idx + 1}`} />
          </div>
        ))}
      </Carousel>

      <h2 className="text-2xl font-semibold">Templates</h2>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {templates.map(t => (
          <TemplateCard key={t.id} template={t} />
        ))}
      </div>
    </div>
  );
}
