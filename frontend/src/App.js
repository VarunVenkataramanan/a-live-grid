import React, { useState, useEffect } from 'react';
import { onAuthStateChanged } from 'firebase/auth';
import { auth } from './Firebase'; // Make sure this is your firebase.js
import Sidebar from './components/Sidebar';
import Chatbot from './components/Chatbot';
import NewsFeed from './components/NewsFeed';
import Header from './components/Header';
import SplashScreen from './components/SplashScreen';
import AuthForm from './components/AuthForm'; // Import your AuthForm
import './App.css';

function App() {
  const [showSplash, setShowSplash] = useState(true);
  const [activeFeed, setActiveFeed] = useState('chat');
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Listen for Firebase auth state changes
  useEffect(() => {
    const unsub = onAuthStateChanged(auth, (firebaseUser) => {
      setUser(firebaseUser);
      setLoading(false);
    });
    return () => unsub();
  }, []);

  const handleFeedChange = (feedType) => {
    setActiveFeed(feedType);
  };

  const renderMainContent = () => {
    switch (activeFeed) {
      case 'report':
        return <NewsFeed />;
      default:
        return <Chatbot />;
    }
  };

  if (loading || showSplash) {
    return <SplashScreen onFinish={() => setShowSplash(false)} />;
  }

  if (!user) {
    return <AuthForm onAuth={() => setUser(auth.currentUser)} />;
  }

  return (
    <div className="app-container">
      <Sidebar onFeedChange={handleFeedChange} />
      <div className="main-content-wrapper">
        <Header />
        <main className="main-content">
          {renderMainContent()}
        </main>
      </div>
    </div>
  );
}

export default App;