import { Link } from "react-router-dom";
import { Scan, Sparkles, Search, BarChart3, ArrowRight } from "lucide-react";

const FEATURES = [
  { icon: Scan, title: "Bookshelf Scanner", desc: "YOLOv8 + EasyOCR detects books from any photo", to: "/scanner", color: "bg-indigo-50 text-indigo-600" },
  { icon: Sparkles, title: "AI Recommendations", desc: "TF-IDF, KNN & collaborative filtering picks", to: "/recommendations", color: "bg-teal-50 text-teal-600" },
  { icon: Search, title: "Semantic Search", desc: "Natural language search via Sentence Transformers", to: "/search", color: "bg-amber-50 text-amber-600" },
  { icon: BarChart3, title: "Reading Analytics", desc: "K-Means clustering reveals your reading patterns", to: "/dashboard", color: "bg-pink-50 text-pink-600" },
];

export default function Home() {
  return (
    <div>
      <div className="text-center py-12">
        <span className="inline-block px-3 py-1 bg-indigo-100 text-indigo-700 text-xs font-medium rounded-full mb-4">
          AI-Powered Book Discovery
        </span>
        <h1 className="text-4xl font-semibold text-gray-900 mb-4">
          📚 ShelfScanner
        </h1>
        <p className="text-lg text-gray-500 max-w-xl mx-auto">
          Photograph any bookshelf. AI detects the books, extracts titles, and recommends your next great read.
        </p>
        <div className="flex justify-center gap-3 mt-6">
          <Link to="/scanner" className="px-6 py-2.5 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700">
            Start Scanning
          </Link>
          <Link to="/search" className="px-6 py-2.5 border border-gray-300 rounded-lg font-medium hover:bg-gray-50">
            Search Books
          </Link>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        {FEATURES.map(({ icon: Icon, title, desc, to, color }) => (
          <Link key={to} to={to} className="group bg-white rounded-xl border border-gray-200 p-5 hover:border-indigo-300 hover:shadow-sm transition-all">
            <div className={`w-10 h-10 rounded-lg ${color} flex items-center justify-center mb-3`}>
              <Icon size={20} />
            </div>
            <h3 className="font-medium text-gray-900 mb-1">{title}</h3>
            <p className="text-sm text-gray-500">{desc}</p>
            <div className="flex items-center gap-1 mt-3 text-indigo-600 text-sm font-medium opacity-0 group-hover:opacity-100 transition-opacity">
              Try it <ArrowRight size={14} />
            </div>
          </Link>
        ))}
      </div>

      <div className="mt-10 bg-gray-900 rounded-xl p-6 text-white">
        <h2 className="font-medium mb-3">🧠 ML Pipeline</h2>
        <div className="flex items-center gap-2 flex-wrap text-sm">
          {["Image Upload", "→", "YOLOv8 Detection", "→", "EasyOCR", "→", "NLP Cleaning", "→", "TF-IDF + Cosine Sim", "→", "Recommendations"].map((s, i) => (
            <span key={i} className={s === "→" ? "text-gray-500" : "px-2 py-1 bg-gray-800 rounded text-gray-200 text-xs"}>
              {s}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}
