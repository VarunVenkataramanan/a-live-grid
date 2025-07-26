import React, { useState } from 'react';
import './Chatbot.css';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const handleSend = (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    
    const userMessage = { from: 'user', text: input };
    setMessages([...messages, userMessage]);
    setInput('');
    
    // Simulate bot response
    setTimeout(() => {
      const botMessage = { from: 'bot', text: 'I understand your message. This is a demo response.' };
      setMessages(prev => [...prev, botMessage]);
    }, 1500);
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
            />
            <button className="send-button" type="submit">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" fill="currentColor"/>
              </svg>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Chatbot; 