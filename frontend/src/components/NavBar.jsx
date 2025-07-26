import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  HomeIcon,
  PlusCircleIcon,
  CollectionIcon,
  FolderIcon,
  PuzzlePieceIcon,
  UserIcon
} from '@heroicons/react/24/outline';

export default function NavBar() {
  const links = [
    { to: '/', icon: HomeIcon, label: 'Home' },
    { to: '/create', icon: PlusCircleIcon, label: 'Create' },
    { to: '/gallery', icon: CollectionIcon, label: 'Gallery' },
    { to: '/projects', icon: FolderIcon, label: 'Projects' },
    { to: '/plugins', icon: PuzzlePieceIcon, label: 'Plugins' },
    { to: '/profile', icon: UserIcon, label: 'Profile' },
  ];

  return (
    <nav className="bg-white shadow-inner">
      <div className="max-w-4xl mx-auto px-4">
        <ul className="flex justify-around">
          {links.map(({ to, icon: Icon, label }) => (
            <li key={to} className="flex-grow">
              <NavLink
                to={to}
                className={({ isActive }) =>
                  `flex flex-col items-center py-2 ${isActive ? 'text-primary' : 'text-gray-500'}`
                }
              >
                <Icon className="h-6 w-6" />
                <span className="text-xs mt-1">{label}</span>
              </NavLink>
            </li>
          ))}
        </ul>
      </div>
    </nav>
  );
                  }
