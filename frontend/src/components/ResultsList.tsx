import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";

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
    <Card className="w-full max-w-md mt-8">
      <CardHeader>
        <CardTitle>Search Results</CardTitle>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-[300px] pr-4">
          {results.map((result) => (
            <div key={result.id} className="mb-4 pb-4 border-b last:border-b-0">
              <h3 className="text-xl font-semibold">{result.name}</h3>
              <p className="text-muted-foreground">{result.profession}</p>
              <p className="text-muted-foreground">{result.location}</p>
            </div>
          ))}
        </ScrollArea>
      </CardContent>
    </Card>
  );
}
