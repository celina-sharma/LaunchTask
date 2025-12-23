'use client';

export default function StatCard({
  title,
  value,
  percentage,
  icon,
  positive = true,
}) {
  return (
    <div className="flex items-center justify-between bg-white rounded-2xl px-6 py-5 shadow-sm">
      {/* Left content */}
      <div>
        <p className="text-sm text-gray-400">{title}</p>

        <div className="flex items-center gap-2 mt-1">
          <h3 className="text-lg font-semibold text-gray-800">
            {value}
          </h3>

          <span
            className={`text-sm font-medium ${
              positive ? 'text-green-500' : 'text-red-500'
            }`}
          >
            {percentage}
          </span>
        </div>
      </div>

      {/* Right icon */}
      <div className="w-12 h-12 rounded-xl bg-teal-400 flex items-center justify-center text-white">
        {icon}
      </div>
    </div>
  );
}
