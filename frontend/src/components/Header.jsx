import React from 'react';
import './Header.css';

const Header = () => {
  return (
    <header className="app-header">
      <div className="header-left">
        <h1 className="header-title"><span className="header-title-bold">A-Live</span><span className="header-title-accent">Grid</span></h1>
      </div>
      <div className="header-right">
        <div className="user-avatar">A</div>
      </div>
    </header>
  );
};

export default Header; 