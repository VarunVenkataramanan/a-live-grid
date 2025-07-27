import React, { useState, useEffect } from 'react';
import './Sidebar.css';

const API_BASE_URL = 'https://livegrid-467013.el.r.appspot.com';

const Sidebar = ({ onFeedChange, onNewsClick }) => {
  const [collapsed, setCollapsed] = useState(false);
  const [activeFeed, setActiveFeed] = useState('chat');
  const [newsPosts, setNewsPosts] = useState([]);
  const [loading, setLoading] = useState(true);

  const handleFeedClick = (feedType) => {
    setActiveFeed(feedType);
    onFeedChange(feedType);
  };

  const handleNewsClick = (postId) => {
    onNewsClick(postId);
    setActiveFeed('report');
    onFeedChange('report');
  };

  // Fetch news posts for sidebar
  const fetchNewsPosts = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/api/v1/posts/short-post`);
      if (!response.ok) {
        throw new Error('Failed to fetch posts');
      }
      const data = await response.json();
      
      // Transform the data to handle Base64 images and ensure proper field mapping
      const transformedPosts = data.map(post => ({
        ...post,
        title: post.title || 'Untitled Post',
        author: post.username || post.author || 'Anonymous',
        date: post.created_at ? new Date(post.created_at).toLocaleDateString() : post.date || 'Unknown'
      }));
      
      setNewsPosts(transformedPosts);
    } catch (err) {
      console.error('Error fetching news posts:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNewsPosts();
  }, []);

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
                className={`sidebar-link ${activeFeed === 'maps' ? 'active' : ''}`}
                onClick={() => handleFeedClick('maps')}
              >
                Live Maps
              </li>
              <li
                className={`sidebar-link ${activeFeed === 'report' ? 'active' : ''}`}
                onClick={() => handleFeedClick('report')}
              >
                Report Feed
              </li>
              <li className="sidebar-divider"></li>
              <li className="sidebar-section-title">Recent News</li>
              {loading ? (
                <li className="sidebar-news-item">Loading...</li>
              ) : (
                newsPosts.slice(0, 10).map(post => (
                  <li
                    key={post.id}
                    className="sidebar-news-item"
                    onClick={() => handleNewsClick(post.id)}
                  >
                    {post.title}
                  </li>
                ))
              )}
            </ul>
          </nav>
        </>
      )}
    </aside>
  );
};

export default Sidebar; 