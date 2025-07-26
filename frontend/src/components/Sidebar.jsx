import React, { useState } from 'react';
import './Sidebar.css';

const Sidebar = ({ onFeedChange }) => {
  const [collapsed, setCollapsed] = useState(false);
  const [activeFeed, setActiveFeed] = useState('chat');

  const handleFeedClick = (feedType) => {
    setActiveFeed(feedType);
    onFeedChange(feedType);
  };

  return (
    <aside className={`sidebar${collapsed ? ' collapsed' : ''}`}>
      <button className="sidebar-toggle" onClick={() => setCollapsed(c => !c)} aria-label="Toggle sidebar">
        <span className="hamburger-icon">
          <span></span>
          <span></span>
          <span></span>
        </span>
      </button>
      <div className="sidebar-header">
        {/* Logo can remain here if needed, but title is removed */}
      </div>
      {!collapsed && (
        <>
          <nav className="sidebar-nav">
            <ul>
              <li
                className={`sidebar-link ${activeFeed === 'chat' ? 'active' : ''}`}
                onClick={() => handleFeedClick('chat')}
              >
                Chat
              </li>
              <li
                className={`sidebar-link ${activeFeed === 'report' ? 'active' : ''}`}
                onClick={() => handleFeedClick('report')}
              >
                Report Feed
              </li>
            </ul>
          </nav>
          <div className="sidebar-news">
            <h2 className="news-title">News</h2>
            <ul className="news-list">
              <li>OpenAI launches new model</li>
              <li>React 19 announced</li>
              <li>AI trends in 2024</li>
            </ul>
          </div>
        </>
      )}
    </aside>
  );
};

export default Sidebar; 