import React, { useState, useRef, useEffect } from 'react';
import { auth } from '../Firebase';
import { signOut } from 'firebase/auth';
import './Header.css';

const Header = ({ onLogout }) => {
  const [showDropdown, setShowDropdown] = useState(false);
  const [user, setUser] = useState(null);
  const dropdownRef = useRef(null);

  useEffect(() => {
    const unsubscribe = auth.onAuthStateChanged((user) => {
      setUser(user);
    });

    return () => unsubscribe();
  }, []);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setShowDropdown(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const handleLogout = async () => {
    try {
      await signOut(auth);
      if (onLogout) {
        onLogout();
      }
    } catch (error) {
      console.error('Error signing out:', error);
    }
  };

  const getUserInitial = () => {
    if (user?.displayName) {
      return user.displayName.charAt(0).toUpperCase();
    }
    if (user?.email) {
      return user.email.charAt(0).toUpperCase();
    }
    return 'U';
  };

  const getUserName = () => {
    if (user?.displayName) {
      return user.displayName;
    }
    if (user?.email) {
      return user.email;
    }
    return 'User';
  };

  return (
    <header className="app-header">
      <div className="header-left">
        <h1 className="header-title"><span className="header-title-bold">A-Live</span><span className="header-title-accent">Grid</span></h1>
      </div>
      <div className="header-right">
        <div className="user-avatar-container" ref={dropdownRef}>
          <button 
            className="user-avatar-button"
            onClick={() => setShowDropdown(!showDropdown)}
            title={getUserName()}
          >
            <div className="user-avatar">{getUserInitial()}</div>
          </button>
          {showDropdown && (
            <div className="user-dropdown">
              <div className="user-info">
                <div className="user-name">{getUserName()}</div>
                <div className="user-email">{user?.email}</div>
              </div>
              <div className="dropdown-divider"></div>
              <button className="dropdown-item logout-button" onClick={handleLogout}>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                  <polyline points="16,17 21,12 16,7"/>
                  <line x1="21" y1="12" x2="9" y2="12"/>
                </svg>
                Logout
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header; 