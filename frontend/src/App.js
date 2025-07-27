import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Chatbot from './components/Chatbot';
import NewsFeed from './components/NewsFeed';
import LiveMaps from './components/LiveMaps';
import Header from './components/Header';
import SplashScreen from './components/SplashScreen';
import AuthForm from './components/AuthForm';
import { auth } from './Firebase';
import { onAuthStateChanged } from 'firebase/auth';
import './App.css';


function App() {
  const [showSplash, setShowSplash] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [activeFeed, setActiveFeed] = useState('chat');
  const [selectedPostId, setSelectedPostId] = useState(null);

  const handleFeedChange = (feedType) => {
    setActiveFeed(feedType);
  };

  // Check authentication state
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setIsAuthenticated(!!user);
      setIsLoading(false);
    });

    return () => unsubscribe();
  }, []);

  const handleAuth = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
  };

  const handleNewsClick = (postId) => {
    setSelectedPostId(postId);
  };

  const renderMainContent = () => {
    switch (activeFeed) {
      case 'report':
        return <NewsFeed selectedPostId={selectedPostId} onPostClose={() => setSelectedPostId(null)} />;
      case 'maps':
        return <LiveMaps />;
      default:
        return <Chatbot />;
    }
  };

  // Show loading while checking authentication
  if (isLoading) {
    return (
      <div className="app-container">
        <div className="loading-container">
          <div className="loading-spinner">
            <div className="spinner"></div>
            <p>Loading...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="app-container">
      {showSplash && <SplashScreen onFinish={() => setShowSplash(false)} />}
      {!showSplash && !isAuthenticated && (
        <div className="auth-page">
          <AuthForm onAuth={handleAuth} />
        </div>
      )}
      {!showSplash && isAuthenticated && (
        <>
          <Sidebar onFeedChange={handleFeedChange} onNewsClick={handleNewsClick} />
          <div className="main-content-wrapper">
            <Header onLogout={handleLogout} />
            <main className="main-content">
              {renderMainContent()}
            </main>
          </div>
        </>
      )}
    </div>
  );
}

export default App;
