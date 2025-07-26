import React, { useEffect } from 'react';
import './SplashScreen.css';

const SplashScreen = ({ onFinish }) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      onFinish();
    }, 1000); // Show splash for 1 second
    return () => clearTimeout(timer);
  }, [onFinish]);

  return (
    <div className="splash-screen">
      <div className="splash-content">
        <img src="./Grid.jpg" alt="A-LiveGrid Logo" className="splash-logo" />
      </div>
    </div>
  );
};

export default SplashScreen; 