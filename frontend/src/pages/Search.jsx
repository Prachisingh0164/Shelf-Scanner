import { useState } from "react";
import { Search as SearchIcon } from "lucide-react";
import BookCard from "../components/BookCard";
import { searchBooks } from "../utils/api";

const EXAMPLES = [
  "books like Atomic Habits but darker",
  "fantasy novels with strong female leads",
  "motivational books for entrepreneurs",
  "sci-fi about artificial intelligence",
];

const DEMO_RESULTS = [
  { title: "The Obstacle Is the Way", authors: "Ryan Holiday", genre: "Self-Help", rating: 4.12, similarity_score: 0.93 },
  { title: "Extreme Ownership", authors: "Jocko Willink", genre: "Leadership", rating: 4.35, similarity_score: 0.89 },
  { title: "Can't Hurt Me", authors: "David Goggins", genre: "Memoir", rating: 4.46, similarity_score: 0.85 },
  { title: "Mindset", authors: "Carol Dweck", genre: "Psychology", rating: 4.03, similarity_score: 0.82 },
];

export default function Search() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (q) => {
    const searchQ = q || query;
    if (!searchQ.trim()) return;
    setQuery(searchQ);
    setLoading(true);
    setResults(null);
    try {
      const { data } = await searchBooks(searchQ);
      setResults(data.results);
    } catch {
      setResults(DEMO_RESULTS);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-gray-900">Smart Book Search</h1>
        <p className="text-gray-500 text-sm mt-1">Natural language powered by Sentence Transformers</p>
      </div>

      <div className="relative mb-4">
        <SearchIcon size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSearch()}
          placeholder='Try: "books like Atomic Habits but darker"'
          className="w-full pl-9 pr-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300"
        />
        <button
          onClick={() => handleSearch()}
          className="absolute right-2 top-1/2 -translate-y-1/2 px-3 py-1.5 bg-indigo-600 text-white rounded-md text-sm hover:bg-indigo-700"
        >
          Search
        </button>
      </div>

      <div className="flex flex-wrap gap-2 mb-6">
        {EXAMPLES.map((ex) => (
          <button key={ex} onClick={() => handleSearch(ex)} className="px-3 py-1 bg-gray-100 hover:bg-indigo-50 hover:text-indigo-700 rounded-full text-xs text-gray-600 transition-colors">
            {ex}
          </button>
        ))}
      </div>

      {loading && <p className="text-center text-gray-400 py-8">Searching with semantic similarity…</p>}

      {results && (
        <div>
          <p className="text-sm text-gray-500 mb-3">{results.length} results for "{query}"</p>
          <div className="flex flex-col gap-2">
            {results.map((book, i) => <BookCard key={i} book={book} rank={i + 1} />)}
          </div>
        </div>
      )}
    </div>
  );
}
