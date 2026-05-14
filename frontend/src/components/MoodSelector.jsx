const MOODS = [
  { key: "happy", emoji: "😄", label: "Happy" },
  { key: "motivational", emoji: "🚀", label: "Motivational" },
  { key: "dark", emoji: "🌑", label: "Dark" },
  { key: "scifi", emoji: "🛸", label: "Sci-Fi" },
  { key: "emotional", emoji: "💙", label: "Emotional" },
];

export default function MoodSelector({ selected, onSelect }) {
  return (
    <div className="grid grid-cols-5 gap-3">
      {MOODS.map((mood) => (
        <button
          key={mood.key}
          onClick={() => onSelect(mood.key)}
          className={`flex flex-col items-center gap-2 p-4 rounded-xl border transition-all ${
            selected === mood.key
              ? "border-indigo-400 bg-indigo-50 shadow-sm"
              : "border-gray-200 bg-white hover:border-indigo-200"
          }`}
        >
          <span className="text-2xl">{mood.emoji}</span>
          <span className="text-xs text-gray-600 font-medium">{mood.label}</span>
        </button>
      ))}
    </div>
  );
}
