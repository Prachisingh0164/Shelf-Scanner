import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from "recharts";

const TREND = [
  { month: "Aug", books: 2 }, { month: "Sep", books: 4 }, { month: "Oct", books: 3 },
  { month: "Nov", books: 6 }, { month: "Dec", books: 5 }, { month: "Jan", books: 4 },
];

const GENRES = [
  { name: "Self-Help", value: 8 }, { name: "Sci-Fi", value: 6 },
  { name: "Biography", value: 5 }, { name: "Fiction", value: 5 },
];

const COLORS = ["#7F77DD", "#1D9E75", "#EF9F27", "#D4537E"];

const RECENT = [
  { title: "Atomic Habits", author: "James Clear", date: "Jan 10" },
  { title: "Sapiens", author: "Yuval Noah Harari", date: "Jan 8" },
  { title: "The Alchemist", author: "Paulo Coelho", date: "Jan 5" },
  { title: "Deep Work", author: "Cal Newport", date: "Dec 28" },
];

export default function Dashboard() {
  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-gray-900">Reading Analytics</h1>
        <p className="text-gray-500 text-sm mt-1">Insights powered by K-Means clustering</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-4 mb-8">
        {[["Books scanned", "24"], ["This month", "6"], ["Avg rating", "4.3"]].map(([label, val]) => (
          <div key={label} className="bg-white rounded-xl border border-gray-200 p-4">
            <p className="text-xs text-gray-500 mb-1">{label}</p>
            <p className="text-2xl font-semibold text-gray-900">{val}</p>
          </div>
        ))}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-2 gap-6 mb-8">
        <div className="bg-white rounded-xl border border-gray-200 p-4">
          <h2 className="text-sm font-medium text-gray-700 mb-4">Reading trend</h2>
          <ResponsiveContainer width="100%" height={160}>
            <BarChart data={TREND}>
              <XAxis dataKey="month" tick={{ fontSize: 11 }} axisLine={false} tickLine={false} />
              <YAxis hide />
              <Tooltip cursor={{ fill: "#EEEDFE" }} />
              <Bar dataKey="books" fill="#7F77DD" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white rounded-xl border border-gray-200 p-4">
          <h2 className="text-sm font-medium text-gray-700 mb-4">Favorite genres</h2>
          <div className="flex items-center gap-4">
            <PieChart width={120} height={120}>
              <Pie data={GENRES} cx={55} cy={55} innerRadius={30} outerRadius={55} dataKey="value" strokeWidth={0}>
                {GENRES.map((_, i) => <Cell key={i} fill={COLORS[i]} />)}
              </Pie>
            </PieChart>
            <div className="flex flex-col gap-2">
              {GENRES.map((g, i) => (
                <div key={g.name} className="flex items-center gap-2">
                  <div className="w-2.5 h-2.5 rounded-full" style={{ background: COLORS[i] }} />
                  <span className="text-xs text-gray-600">{g.name}</span>
                  <span className="text-xs text-gray-400 ml-auto">{g.value}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Recent scans */}
      <div className="bg-white rounded-xl border border-gray-200 p-4">
        <h2 className="text-sm font-medium text-gray-700 mb-3">Recent scans</h2>
        <div className="flex flex-col divide-y divide-gray-100">
          {RECENT.map((book) => (
            <div key={book.title} className="flex justify-between items-center py-2.5">
              <div>
                <p className="text-sm font-medium text-gray-800">{book.title}</p>
                <p className="text-xs text-gray-400">{book.author}</p>
              </div>
              <span className="text-xs text-gray-400">{book.date}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
