"use client";

import { useState } from "react";
import SearchDialog from "@/components/SearchDialog";
import ResultsList from "@/components/ResultsList";

export default function Home() {
  const [results, setResults] = useState([]);

  const handleSearch = async (query: string) => {
    // TODO: Replace with actual API call
    // Dummy data for demonstration purposes
    const dummyResults = [
      {
        id: "1",
        name: "John Doe",
        profession: "Software Engineer",
        location: "San Francisco, CA",
      },
      {
        id: "2",
        name: "Jane Smith",
        profession: "Marketing Specialist",
        location: "New York, NY",
      },
      {
        id: "3",
        name: "Alex Johnson",
        profession: "Graphic Designer",
        location: "London, UK",
      },
      {
        id: "4",
        name: "Emily Brown",
        profession: "Data Analyst",
        location: "Toronto, Canada",
      },
      {
        id: "5",
        name: "Michael Lee",
        profession: "Product Manager",
        location: "Seattle, WA",
      },
    ];

    // Simulate API call delay
    await new Promise((resolve) => setTimeout(resolve, 500));

    // Filter results based on query (case-insensitive)
    const filteredResults = dummyResults.filter(
      (result) =>
        result.name.toLowerCase().includes(query.toLowerCase()) ||
        result.profession.toLowerCase().includes(query.toLowerCase()) ||
        result.location.toLowerCase().includes(query.toLowerCase())
    );

    setResults(filteredResults);
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <h1 className="text-4xl font-bold mb-8">People Search</h1>
      <SearchDialog onSearch={handleSearch} />
      <ResultsList results={results} />
    </main>
  );
}
