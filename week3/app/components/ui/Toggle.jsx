"use client";

import { useState } from "react";

export function Toggle({ label, defaultChecked = false }) {
  const [enabled, setEnabled] = useState(defaultChecked);

  return (
    <div className="flex items-center justify-between">
      <span
        className={`text-sm transition
          ${enabled ? "text-gray-700" : "text-gray-400"}
        `}
      >
        {label}
      </span>

      {/* TOGGLE */}
      <button
        type="button"
        onClick={() => setEnabled(!enabled)}
        className={`relative inline-flex h-5 w-10 rounded-2xl transition-colors
          ${enabled ? "bg-teal-400" : "bg-gray-200"}
        `}
      >
        <span
          className={`inline-block h-5 w-5 bg-white rounded-full shadow
            transform transition
            ${enabled ? "translate-x-5" : "translate-x-1"}
          `}
        />
      </button>
    </div>
  );
}
