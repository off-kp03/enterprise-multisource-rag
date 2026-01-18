type Props = {
  role: "user" | "assistant";
  content: string;
};

export default function ChatBubble({ role, content }: Props) {
  const isUser = role === "user";

  return (
    <div
      className={`flex ${isUser ? "justify-end" : "justify-start"} mb-2`}
    >
      <div
        className={`max-w-lg px-4 py-2 rounded-lg ${
          isUser
            ? "bg-black text-white"
            : "bg-gray-200 text-black"
        }`}
      >
        {content}
      </div>
    </div>
  );
}
