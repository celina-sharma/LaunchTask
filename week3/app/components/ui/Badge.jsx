export default function Badge({ text, color = "green" }) {
  const colors = {
    green: "bg-green-100 text-green-600",
    red: "bg-red-100 text-red-600",
    yellow: "bg-yellow-100 text-yellow-600",
    blue: "bg-blue-100 text-blue-600",
    gray: "bg-gray-100 text-gray-600",
  };

  return (
    <span
      className={`text-xs font-semibold px-3 py-1 rounded-full ${
        colors[color] || colors.gray
      }`}
    >
      {text}
    </span>
  );
}
