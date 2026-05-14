import { Star } from "lucide-react";

export default function BookCard({ book, rank }) {
  return (
    <div className="flex items-center gap-3 p-3 bg-white rounded-lg border border-gray-200 hover:border-indigo-300 transition-colors">
      {rank && (
        <span className="w-7 h-7 rounded-full bg-indigo-50 text-indigo-700 text-xs font-semibold flex items-center justify-center flex-shrink-0">
          {rank}
        </span>
      )}
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-gray-900 truncate">{book.title}</p>
        <p className="text-xs text-gray-500 mt-0.5">
          {book.authors || book.author}
          {book.genre && ` · ${book.genre}`}
        </p>
      </div>
      {book.rating && (
        <div className="flex items-center gap-1 text-amber-500 flex-shrink-0">
          <Star size={12} fill="currentColor" />
          <span className="text-xs font-medium">{parseFloat(book.rating).toFixed(1)}</span>
        </div>
      )}
      {book.similarity_score && (
        <span className="text-xs font-semibold text-indigo-600 flex-shrink-0">
          {Math.round(book.similarity_score * 100)}%
        </span>
      )}
    </div>
  );
}
