import React from 'react';
import ChatInterface from './components/ChatInterface';

function App() {
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      <header className="bg-white shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8 flex items-center justify-between">
          <h1 className="text-xl font-bold text-gray-900 flex items-center gap-2">
            <span className="text-indigo-600">🛍️</span> Shopify AI Agent
          </h1>
        </div>
      </header>

      <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:px-6 lg:px-8">
        <ChatInterface />
      </main>
    </div>
  );
}

export default App;
