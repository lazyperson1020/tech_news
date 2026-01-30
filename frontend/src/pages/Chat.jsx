import { useState, useEffect, useRef } from 'react';
import useAuthStore from '../store/authStore';
import api from '../services/api';
import '../styles/Chat.css';

function Chat() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const messagesEndRef = useRef(null);
  const { isAuthenticated } = useAuthStore();

  // Load chat history on component mount
  useEffect(() => {
    if (isAuthenticated) {
      loadChatHistory();
    }
  }, [isAuthenticated]);

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const loadChatHistory = async () => {
    try {
      const response = await api.get('/chat/history/');
      // Reverse to show oldest first
      setMessages(response.data.reverse());
    } catch (err) {
      console.error('Failed to load chat history:', err);
      setError('Failed to load chat history');
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();

    if (!inputValue.trim()) {
      return;
    }

    const userInput = inputValue;
    setInputValue('');
    setError('');
    setLoading(true);

    try {
      const response = await api.post('/chat/send_message/', {
        message: userInput,
      });

      // Add both user and assistant messages
      setMessages((prev) => [
        ...prev,
        response.data.user_message,
        response.data.assistant_message,
      ]);
    } catch (err) {
      console.error('Failed to send message:', err);
      setError(
        err.response?.data?.error ||
          'Failed to send message. Please try again.'
      );
      // Re-add the input value so user can retry
      setInputValue(userInput);
    } finally {
      setLoading(false);
    }
  };

  const handleClearHistory = async () => {
    if (
      !window.confirm(
        'Are you sure you want to clear all chat history? This cannot be undone.'
      )
    ) {
      return;
    }

    try {
      await api.delete('/chat/clear/');
      setMessages([]);
      setError('');
    } catch (err) {
      console.error('Failed to clear chat history:', err);
      setError('Failed to clear chat history');
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="chat-container">
        <div className="chat-message system-message">
          Please log in to use the chat feature.
        </div>
      </div>
    );
  }

  return (
    <div className="chat-wrapper">
      <div className="chat-header">
        <h1>Chat with AI Assistant</h1>
        <button
          onClick={handleClearHistory}
          className="clear-button"
          title="Clear chat history"
        >
          Clear History
        </button>
      </div>

      <div className="chat-container">
        {messages.length === 0 && (
          <div className="chat-message system-message">
            Start a conversation! Ask questions about technology, news, or anything else.
          </div>
        )}

        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`chat-message ${
              msg.role === 'user' ? 'user-message' : 'assistant-message'
            }`}
          >
            <div className="message-content">{msg.content}</div>
            <div className="message-time">
              {new Date(msg.created_at).toLocaleTimeString()}
            </div>
          </div>
        ))}

        {loading && (
          <div className="chat-message assistant-message loading">
            <div className="message-content">
              <span className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </span>
            </div>
          </div>
        )}

        {error && (
          <div className="chat-message error-message">
            <div className="message-content">
              <strong>Error:</strong> {error}
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSendMessage} className="chat-input-form">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Type your message here..."
          disabled={loading}
          className="chat-input"
        />
        <button
          type="submit"
          disabled={loading || !inputValue.trim()}
          className="send-button"
        >
          {loading ? 'Sending...' : 'Send'}
        </button>
      </form>
    </div>
  );
}

export default Chat;
