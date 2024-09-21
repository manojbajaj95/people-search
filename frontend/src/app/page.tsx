"use client";

import { useState } from "react";
import SearchDialog from "@/components/SearchDialog";
import ResultsList from "@/components/ResultsList";

export default function Home() {
  const [results, setResults] = useState([]);

  const handleSearch = async (query: string) => {
    // TODO: Replace with actual API call
    const response = await fetch("/api/search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });
    const data = await response.json();
    setResults(data.results);
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <h1 className="text-4xl font-bold mb-8">People Search</h1>
      <SearchDialog onSearch={handleSearch} />
      <ResultsList results={results} />
    </main>
  );
}
