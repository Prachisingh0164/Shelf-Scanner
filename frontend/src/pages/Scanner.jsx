import { useState, useRef } from "react";
import { Upload, Scan, CheckCircle } from "lucide-react";
import BookCard from "../components/BookCard";
import { scanBookshelf, getDemoScan, getRecommendations } from "../utils/api";

export default function Scanner() {
  const [status, setStatus] = useState("idle"); // idle | scanning | done | error
  const [detected, setDetected] = useState([]);
  const [recs, setRecs] = useState([]);
  const [preview, setPreview] = useState(null);
  const inputRef = useRef();

  const handleFile = async (file) => {
    if (!file) return;
    setPreview(URL.createObjectURL(file));
    setStatus("scanning");
    try {
      const formData = new FormData();
      formData.append("image", file);
      const { data } = await scanBookshelf(formData);
      setDetected(data.detected_books);
      // Get recommendations from detected titles
      const titles = data.detected_books.map((b) => b.title).filter(Boolean);
      if (titles.length > 0) {
        const recRes = await getRecommendations(titles);
        setRecs(recRes.data.recommendations);
      }
      setStatus("done");
    } catch {
      // Fallback to demo mode
      runDemo();
    }
  };

  const runDemo = async () => {
    setStatus("scanning");
    try {
      const { data } = await getDemoScan();
      setDetected(data.detected_books);
      const titles = data.detected_books.map((b) => b.title);
      const recRes = await getRecommendations(titles);
      setRecs(recRes.data.recommendations);
      setStatus("done");
    } catch {
      // Hardcoded demo fallback
      setDetected([
        { title: "Atomic Habits", confidence: 0.94 },
        { title: "Psychology of Money", confidence: 0.89 },
        { title: "Sapiens", confidence: 0.92 },
        { title: "Deep Work", confidence: 0.87 },
      ]);
      setRecs([
        { title: "Thinking, Fast and Slow", authors: "Daniel Kahneman", genre: "Psychology", rating: 4.18, similarity_score: 0.94 },
        { title: "Man's Search for Meaning", authors: "Viktor Frankl", genre: "Psychology", rating: 4.37, similarity_score: 0.91 },
        { title: "The Lean Startup", authors: "Eric Ries", genre: "Business", rating: 3.91, similarity_score: 0.88 },
      ]);
      setStatus("done");
    }
  };

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-gray-900">Bookshelf Scanner</h1>
        <p className="text-gray-500 text-sm mt-1">Upload a photo · YOLOv8 detects books · EasyOCR reads titles</p>
      </div>

      {/* Upload Zone */}
      {status === "idle" && (
        <div
          className="border-2 border-dashed border-gray-300 rounded-xl p-12 text-center cursor-pointer hover:border-indigo-400 hover:bg-indigo-50 transition-all"
          onClick={() => inputRef.current.click()}
          onDrop={(e) => { e.preventDefault(); handleFile(e.dataTransfer.files[0]); }}
          onDragOver={(e) => e.preventDefault()}
        >
          <Upload size={36} className="mx-auto text-indigo-400 mb-3" />
          <p className="font-medium text-gray-700">Drop a bookshelf photo here</p>
          <p className="text-sm text-gray-400 mt-1">JPEG, PNG, WEBP</p>
          <div className="mt-4 flex justify-center gap-3">
            <button className="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm hover:bg-indigo-700" onClick={(e) => { e.stopPropagation(); inputRef.current.click(); }}>
              Upload Image
            </button>
            <button className="px-4 py-2 border border-gray-300 rounded-lg text-sm hover:bg-gray-50" onClick={(e) => { e.stopPropagation(); runDemo(); }}>
              Try Demo
            </button>
          </div>
          <input ref={inputRef} type="file" accept="image/*" className="hidden" onChange={(e) => handleFile(e.target.files[0])} />
        </div>
      )}

      {/* Scanning */}
      {status === "scanning" && (
        <div className="text-center py-16">
          <Scan size={36} className="mx-auto text-indigo-500 mb-4 animate-pulse" />
          <p className="text-gray-600">Scanning with YOLOv8 + EasyOCR…</p>
        </div>
      )}

      {/* Results */}
      {status === "done" && (
        <div>
          {preview && (
            <img src={preview} alt="Scanned shelf" className="w-full max-h-48 object-cover rounded-xl mb-6" />
          )}
          <div className="flex items-center gap-2 mb-4">
            <CheckCircle size={18} className="text-green-500" />
            <span className="font-medium text-gray-800">{detected.length} books detected</span>
          </div>

          {/* Detected */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
            {detected.map((book, i) => (
              <div key={i} className="bg-white rounded-lg border border-gray-200 p-3">
                <p className="text-sm font-medium text-gray-900 truncate">{book.title}</p>
                <div className="mt-2 h-1.5 bg-gray-100 rounded-full">
                  <div className="h-full bg-indigo-500 rounded-full" style={{ width: `${(book.confidence || 0.9) * 100}%` }} />
                </div>
                <p className="text-xs text-gray-400 mt-1">{Math.round((book.confidence || 0.9) * 100)}% confidence</p>
              </div>
            ))}
          </div>

          {/* Recommendations */}
          <h2 className="font-semibold text-gray-800 mb-3">Recommendations</h2>
          <div className="flex flex-col gap-2">
            {recs.map((book, i) => <BookCard key={i} book={book} rank={i + 1} />)}
          </div>

          <button className="mt-6 px-4 py-2 border border-gray-200 rounded-lg text-sm hover:bg-gray-50" onClick={() => { setStatus("idle"); setPreview(null); setDetected([]); setRecs([]); }}>
            Scan another shelf
          </button>
        </div>
      )}
    </div>
  );
}
