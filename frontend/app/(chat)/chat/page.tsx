"use client";

import { useState } from "react";
import ChatBubble from "@/components/ChatBubble";
import ChatInput from "@/components/ChatInput";
import { apiPost } from "@/lib/api";

type Message = {
  role: "user" | "assistant";
  content: string;
};

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  async function sendMessage(question: string) {
    setMessages((prev) => [
      ...prev,
      { role: "user", content: question },
    ]);
    setLoading(true);

    try {
      const res = await apiPost<{
        answer: string;
      }>("/rag", { question }, true);

      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: res.answer },
      ]);
    } catch (err: any) {
      alert(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex flex-col">
      <div className="flex-1 p-4 overflow-y-auto">
        {messages.map((m, i) => (
          <ChatBubble
            key={i}
            role={m.role}
            content={m.content}
          />
        ))}
      </div>

      <div className="p-4 border-t">
        <ChatInput onSend={sendMessage} loading={loading} />
      </div>
    </div>
  );
}
