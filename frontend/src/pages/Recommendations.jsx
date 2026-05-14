import { useState } from "react";
import MoodSelector from "../components/MoodSelector";
import BookCard from "../components/BookCard";
import { getMoodRecommendations, getTrending } from "../utils/api";

const DEMO_TRENDING = [
  { title: "Atomic Habits", authors: "James Clear", genre: "Self-Help", rating: 4.37 },
  { title: "The Psychology of Money", authors: "Morgan Housel", genre: "Finance", rating: 4.31 },
  { title: "Sapiens", authors: "Yuval Noah Harari", genre: "History", rating: 4.40 },
  { title: "Dune", authors: "Frank Herbert", genre: "Sci-Fi", rating: 4.26 },
  { title: "Deep Work", authors: "Cal Newport", genre: "Self-Help", rating: 4.17 },
];

export default function Recommendations() {
  const [mood, setMood] = useState(null);
  const [recs, setRecs] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleMood = async (m) => {
    setMood(m);
    setLoading(true);
    try {
      const { data } = await getMoodRecommendations(m);
      setRecs(data.recommendations);
    } catch {
      // Demo fallback per mood
      const demoMap = {
        happy: [{ title: "The Hitchhiker's Guide", authors: "Douglas Adams", genre: "Comedy", rating: 4.22 }],
        motivational: [{ title: "Can't Hurt Me", authors: "David Goggins", genre: "Memoir", rating: 4.46 }],
        dark: [{ title: "1984", authors: "George Orwell", genre: "Dystopia", rating: 4.19 }],
        scifi: [{ title: "Dune", authors: "Frank Herbert", genre: "Sci-Fi", rating: 4.26 }],
        emotional: [{ title: "The Kite Runner", authors: "Khaled Hosseini", genre: "Fiction", rating: 4.30 }],
      };
      setRecs(demoMap[m] || DEMO_TRENDING);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-gray-900">Book Recommendations</h1>
        <p className="text-gray-500 text-sm mt-1">Powered by BERT · Sentiment Analysis · Collaborative Filtering</p>
      </div>

      <h2 className="font-medium text-gray-700 mb-3">How are you feeling today?</h2>
      <MoodSelector selected={mood} onSelect={handleMood} />

      {loading && <div className="text-center py-8 text-gray-400">Finding the perfect books for your mood…</div>}

      {recs && !loading && (
        <div className="mt-6">
          <h2 className="font-semibold text-gray-800 mb-3 capitalize">Books for {mood} mood</h2>
          <div className="flex flex-col gap-2">
            {recs.map((book, i) => <BookCard key={i} book={book} rank={i + 1} />)}
          </div>
        </div>
      )}

      <div className="mt-10">
        <h2 className="font-semibold text-gray-800 mb-3">📈 Trending now</h2>
        <div className="flex flex-col gap-2">
          {DEMO_TRENDING.map((book, i) => <BookCard key={i} book={book} rank={i + 1} />)}
        </div>
      </div>
    </div>
  );
}
