import React from 'react';
import { NavLink } from 'react-router-dom';

const NavBar: React.FC = () => {
  return (
    <nav className="bg-gray-800 p-4 text-white flex space-x-4">
      <NavLink
        to="/dashboard"
        className={({ isActive }) =>
          isActive ? 'underline font-bold' : 'hover:underline'
        }
      >
        Dashboard
      </NavLink>
      <NavLink
        to="/transactions"
        className={({ isActive }) =>
          isActive ? 'underline font-bold' : 'hover:underline'
        }
      >
        Transactions
      </NavLink>
      <NavLink
        to="/profile"
        className={({ isActive }) =>
          isActive ? 'underline font-bold' : 'hover:underline'
        }
      >
        Profile
      </NavLink>
      <NavLink
        to="/ai"
        className={({ isActive }) =>
          isActive ? 'underline font-bold' : 'hover:underline'
        }
      >
        AI Assistant
      </NavLink>
    </nav>
  );
};

export default NavBar;
