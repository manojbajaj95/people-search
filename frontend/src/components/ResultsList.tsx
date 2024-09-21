interface Result {
  id: string;
  name: string;
  profession: string;
  location: string;
}

interface ResultsListProps {
  results: Result[];
}

export default function ResultsList({ results }: ResultsListProps) {
  if (results.length === 0) {
    return null;
  }

  return (
    <div className="w-full max-w-md mt-8">
      <h2 className="text-2xl font-bold mb-4">Search Results</h2>
      <ul className="bg-white shadow-md rounded px-8 pt-6 pb-8">
        {results.map((result) => (
          <li key={result.id} className="mb-4 pb-4 border-b last:border-b-0">
            <h3 className="text-xl font-semibold">{result.name}</h3>
            <p className="text-gray-600">{result.profession}</p>
            <p className="text-gray-500">{result.location}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
