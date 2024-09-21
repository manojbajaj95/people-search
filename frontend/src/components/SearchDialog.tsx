import { useState } from "react";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";

interface SearchDialogProps {
  onSearch: (query: string) => void;
}

export default function SearchDialog({ onSearch }: SearchDialogProps) {
  const [query, setQuery] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(query);
    setQuery("");
  };

  return (
    <Card className="w-full max-w-md">
      <form onSubmit={handleSubmit}>
        <CardContent className="pt-6">
          <div className="space-y-2">
            <Label htmlFor="query">Search Query</Label>
            <Input
              id="query"
              type="text"
              placeholder="E.g., Freelance marketing professional in New York"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
          </div>
        </CardContent>
        <CardFooter>
          <Button type="submit" className="w-full">
            Search
          </Button>
        </CardFooter>
      </form>
    </Card>
  );
}
