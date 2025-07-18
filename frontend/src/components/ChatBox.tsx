import React, { useState } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext.tsx';
import { Link } from 'react-router-dom';

const ChatBox: React.FC = () => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<{ sender: string; text: string }[]>([]);
  const { token } = useAuth();

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMessage = { sender: 'user', text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');

    try {
      const response = await axios.post(
        '/ai/chat',
        { message: input },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      const botMessage = { sender: 'bot', text: response.data.reply };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = { sender: 'bot', text: 'Error getting response from AI.' };
      setMessages((prev) => [...prev, errorMessage]);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="p-4 max-w-md mx-auto border rounded shadow">
      <nav className="mb-4 flex justify-between items-center">
        <h2 className="text-2xl font-bold">AI Budget Advice Chat</h2>
        <Link
          to="/dashboard"
          className="text-blue-600 hover:underline"
        >
          Back to Dashboard
        </Link>
      </nav>
      <div className="h-64 overflow-y-auto border p-2 mb-4 bg-gray-50">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`mb-2 p-2 rounded ${
              msg.sender === 'user' ? 'bg-blue-200 text-right' : 'bg-green-200 text-left'
            }`}
          >
            {msg.text}
          </div>
        ))}
      </div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Ask your budget question..."
        className="border p-2 w-full mb-2"
      />
      <button
        onClick={sendMessage}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 w-full"
      >
        Send
      </button>
    </div>
  );
};

export default ChatBox;
