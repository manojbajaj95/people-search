"use client";

import { useState } from "react";

export default function Home() {
  const [query, setQuery] = useState("");
  const [users, setUsers] = useState([]);

  const handleSearch = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    // This is a mock API call. In a real application, you'd fetch from an actual API
    const mockUsers = [
      { id: 1, name: "John Doe", email: "john@example.com" },
      { id: 2, name: "Jane Smith", email: "jane@example.com" },
      { id: 3, name: "Bob Johnson", email: "bob@example.com" },
    ].filter((user) => user.name.toLowerCase().includes(query.toLowerCase()));
    setUsers(mockUsers);
  };

  return (
    <div className="flex flex-col items-center min-h-screen p-8">
      <form onSubmit={handleSearch} className="w-full max-w-xl mb-8">
        <div className="flex items-center border border-gray-300 rounded-full overflow-hidden">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full px-4 py-2 focus:outline-none"
            placeholder="Search for users..."
          />
          <button type="submit" className="px-4 py-2 bg-blue-500 text-white">
            Search
          </button>
        </div>
      </form>
      <div className="w-full max-w-xl">
        {users.map((user) => (
          <div
            key={user.id}
            className="mb-4 p-4 border border-gray-300 rounded"
          >
            <h2 className="text-xl font-bold">{user.name}</h2>
            <p className="text-gray-600">{user.email}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
