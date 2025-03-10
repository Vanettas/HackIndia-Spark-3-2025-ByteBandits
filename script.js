import { useState } from "react";
import { Input } from "./ui/Input";
import { Button } from "./ui/Button";

export default function SearchBar({ onSearch }) {
  const [query, setQuery] = useState("");

  return (
    <div className="flex items-center space-x-2">
      <Input
        placeholder="Search documents..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <Button onClick={() => onSearch(query)}>Search</Button>
    </div>
  );
}
