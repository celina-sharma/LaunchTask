export default function InfoCard() {
  return (
    <div className="bg-white rounded-2xl p-6 h-64 flex flex-col justify-between">
      <div>
        <p className="text-xs text-gray-400 mb-1">Built by developers</p>

        <h3 className="text-lg font-semibold text-gray-800">
          Purity UI Dashboard
        </h3>

        <p className="text-sm text-gray-400 mt-2 leading-relaxed">
          From colors, cards, typography to complex elements,<br />you will find
          the full documentation.
        </p>
      </div>

      <span className="text-sm font-medium text-gray-800 cursor-pointer">
        Read more →
      </span>
    </div>
  );
}
