import { Send, Sparkles } from "lucide-react";

function ChatBox({ message, setMessage, onSend, loading }) {
  const handleSubmit = (e) => {
    e.preventDefault();

    if (!message.trim() || loading) {
      return;
    }

    onSend();
  };

  return (
    <form className="chat-box" onSubmit={handleSubmit}>
      <div className="chat-icon">
        <Sparkles size={20} />
      </div>

      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Tell me what you're looking for..."
      />

      <button type="submit" disabled={loading}>
        <Send size={18} />
      </button>
    </form>
  );
}

export default ChatBox;