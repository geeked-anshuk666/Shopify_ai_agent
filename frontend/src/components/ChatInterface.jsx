import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Send, Bot, User, Loader2, AlertCircle } from 'lucide-react';

export default function ChatInterface() {
    const [messages, setMessages] = useState([
        { role: 'agent', content: 'Hello! I am your Shopify Data Analyst. Ask me about orders, products, or customers.' }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!input.trim() || isLoading) return;

        const userMessage = input.trim();
        setInput('');
        setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
        setIsLoading(true);

        try {
            const response = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: userMessage }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            setMessages(prev => [...prev, { role: 'agent', content: data.response }]);
        } catch (error) {
            console.error('Error:', error);
            setMessages(prev => [...prev, {
                role: 'agent',
                content: 'Sorry, I encountered an error creating your response. Please try again.',
                isError: true
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-[calc(100vh-8rem)] bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-4 space-y-6 bg-gray-50">
                {messages.map((message, index) => (
                    <div
                        key={index}
                        className={`flex items-start gap-3 ${message.role === 'user' ? 'flex-row-reverse' : 'flex-row'
                            }`}
                    >
                        <div
                            className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${message.role === 'user'
                                    ? 'bg-indigo-600 text-white'
                                    : message.isError
                                        ? 'bg-red-100 text-red-600'
                                        : 'bg-emerald-600 text-white'
                                }`}
                        >
                            {message.role === 'user' ? <User size={18} /> :
                                message.isError ? <AlertCircle size={18} /> : <Bot size={18} />}
                        </div>

                        <div
                            className={`max-w-[80%] rounded-2xl px-4 py-3 shadow-sm ${message.role === 'user'
                                    ? 'bg-indigo-600 text-white'
                                    : message.isError
                                        ? 'bg-red-50 text-red-800 border border-red-200'
                                        : 'bg-white text-gray-800 border border-gray-100'
                                }`}
                        >
                            {message.role === 'user' ? (
                                <p className="whitespace-pre-wrap">{message.content}</p>
                            ) : (
                                <div className="prose prose-sm max-w-none dark:prose-invert">
                                    <ReactMarkdown
                                        remarkPlugins={[remarkGfm]}
                                        components={{
                                            table: ({ node, ...props }) => (
                                                <div className="overflow-x-auto my-4 border rounded-lg">
                                                    <table className="min-w-full divide-y divide-gray-200" {...props} />
                                                </div>
                                            ),
                                            thead: ({ node, ...props }) => <thead className="bg-gray-50" {...props} />,
                                            th: ({ node, ...props }) => (
                                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider" {...props} />
                                            ),
                                            td: ({ node, ...props }) => (
                                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 border-t border-gray-100" {...props} />
                                            ),
                                        }}
                                    >
                                        {message.content}
                                    </ReactMarkdown>
                                </div>
                            )}
                        </div>
                    </div>
                ))}
                {isLoading && (
                    <div className="flex items-start gap-3">
                        <div className="w-8 h-8 rounded-full bg-emerald-600 text-white flex items-center justify-center shrink-0">
                            <Loader2 size={18} className="animate-spin" />
                        </div>
                        <div className="bg-white rounded-2xl px-4 py-3 shadow-sm border border-gray-100">
                            <span className="text-gray-500 text-sm">Thinking...</span>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="p-4 bg-white border-t border-gray-200">
                <form onSubmit={handleSubmit} className="flex gap-2 relative">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Ask about orders, products, etc..."
                        className="flex-1 p-3 pr-12 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                        disabled={isLoading}
                    />
                    <button
                        type="submit"
                        disabled={isLoading || !input.trim()}
                        className="absolute right-2 top-2 bottom-2 aspect-square flex items-center justify-center bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                        <Send size={18} />
                    </button>
                </form>
            </div>
        </div>
    );
}
