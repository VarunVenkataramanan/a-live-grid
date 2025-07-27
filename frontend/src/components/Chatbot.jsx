import React, { useState } from 'react';
import './Chatbot.css';

const API_BASE_URL = 'https://8fa74c4d7046.ngrok-free.app';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    
    const userMessage = { from: 'user', text: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    
    try {
      const response = await fetch(`${API_BASE_URL}/call_agent`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          thread_id: 'ge4tw5',
          user_input: input
        }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      
      // Add bot response to messages
      const botMessage = { 
        from: 'bot', 
        text: data.response || data.message || 'I received your message but couldn\'t process it properly.'
      };
      setMessages(prev => [...prev, botMessage]);
      
    } catch (error) {
      console.error('Error calling agent:', error);
      let errorText = 'Sorry, I\'m having trouble connecting right now. Please try again later.';
      
      if (error.name === 'TypeError' && error.message.includes('Failed to fetch')) {
        errorText = 'Network error: Unable to connect to the server. Please check your connection.';
      } else if (error.message.includes('CORS')) {
        errorText = 'CORS error: The server is not allowing cross-origin requests.';
      } else if (error.message.includes('415')) {
        errorText = 'Server error: Unsupported media type. The server expects JSON data.';
      } else if (error.message.includes('HTTP error')) {
        errorText = `Server error: ${error.message}`;
      }
      
      const errorMessage = { 
        from: 'bot', 
        text: errorText
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chatbot-container">
      <div className="chatbot-content">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <h1>Hello, Aum</h1>
            <p>I'm <span className="sidebar-title-bold">A-Live</span><span className="sidebar-title-accent">Grid</span>. How can I help you today?</p>
          </div>
        ) : (
          <div className="chatbot-messages">
            {messages.map((msg, idx) => (
              <div key={idx} className={`chatbot-message ${msg.from}`}>
                <div className="message-content">{msg.text}</div>
              </div>
            ))}
          </div>
        )}
      </div>
      
      <div className="chatbot-input-container">
        <form className="chatbot-input-area" onSubmit={handleSend}>
          <div className="input-wrapper">
            <input
              className="chatbot-input"
              type="text"
              value={input}
              onChange={e => setInput(e.target.value)}
              placeholder="Ask A-LiveGrid"
              disabled={isLoading}
            />
            <button className="send-button" type="submit" disabled={isLoading}>
              {isLoading ? (
                <div className="loading-dots">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              ) : (
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                  <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" fill="currentColor"/>
                </svg>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Chatbot; 