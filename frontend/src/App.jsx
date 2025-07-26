import React, { Suspense } from 'react';
import './i18n';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Create from './pages/Create';
import Gallery from './pages/Gallery';
import Projects from './pages/Projects';
import Plugins from './pages/Plugins';
import Profile from './pages/Profile';
import NavBar from './components/NavBar';
import Header from './components/Header';
import Telemetry from './components/Telemetry';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

export default function App() {
  return (
    <Suspense fallback={<div className="flex items-center justify-center h-screen">Loading...</div>}>
      <BrowserRouter>
        <div className="flex flex-col min-h-screen bg-gray-50">
          <Header />
          <Telemetry />
          <div className="flex-grow">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/create" element={<Create />} />
              <Route path="/gallery" element={<Gallery />} />
              <Route path="/projects" element={<Projects />} />
              <Route path="/plugins" element={<Plugins />} />
              <Route path="/profile" element={<Profile />} />
            </Routes>
          </div>
          <NavBar />
          <ToastContainer position="bottom-right" />
        </div>
      </BrowserRouter>
    </Suspense>
  );
}
