import { Link, useLocation } from "react-router-dom";
import { BookOpen, Scan, Sparkles, Search, BarChart3 } from "lucide-react";

const links = [
  { to: "/", label: "Home", icon: BookOpen },
  { to: "/scanner", label: "Scanner", icon: Scan },
  { to: "/recommendations", label: "Discover", icon: Sparkles },
  { to: "/search", label: "Search", icon: Search },
  { to: "/dashboard", label: "Analytics", icon: BarChart3 },
];

export default function Navbar() {
  const { pathname } = useLocation();
  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-5xl mx-auto px-4 flex items-center h-14 gap-6">
        <Link to="/" className="flex items-center gap-2 font-semibold text-indigo-700">
          <BookOpen size={20} />
          ShelfScanner
        </Link>
        <div className="flex gap-1 ml-4">
          {links.map(({ to, label, icon: Icon }) => (
            <Link
              key={to}
              to={to}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-sm transition-colors ${
                pathname === to
                  ? "bg-indigo-50 text-indigo-700 font-medium"
                  : "text-gray-600 hover:bg-gray-100"
              }`}
            >
              <Icon size={15} />
              {label}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  );
}
