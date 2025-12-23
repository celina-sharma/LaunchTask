export default function Progress({ value }) {
  return (
    <div className="w-full bg-gray-200 rounded-full h-1.5">
      <div
        className="bg-teal-400 h-1.5 rounded-full transition-all"
        style={{ width: `${value}%` }}
      />
    </div>
  );
}
 