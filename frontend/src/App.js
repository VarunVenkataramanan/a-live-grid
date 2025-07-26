import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import Chatbot from './components/Chatbot';
import NewsFeed from './components/NewsFeed';
import Header from './components/Header';
import SplashScreen from './components/SplashScreen';
import './App.css';

function App() {
  const [showSplash, setShowSplash] = useState(true);
  const [activeFeed, setActiveFeed] = useState('chat');

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

  return (
    <div className="app-container">
      {showSplash && <SplashScreen onFinish={() => setShowSplash(false)} />}
      {!showSplash && (
        <>
          <Sidebar onFeedChange={handleFeedChange} />
          <div className="main-content-wrapper">
            <Header />
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
