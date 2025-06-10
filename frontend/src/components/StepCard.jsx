import { useState } from "react";
import { ChevronDownIcon, ChevronRightIcon } from "@heroicons/react/20/solid";

export default function StepCard({ row }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="bg-white shadow rounded-md">
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between px-4 py-3 text-left"
      >
        <div>
          <span className="font-semibold text-indigo-600 mr-2">
            {row.step}.
          </span>
          <span className="font-medium">{row.action}</span>
        </div>
        {open ? (
          <ChevronDownIcon className="h-5 w-5 text-gray-400" />
        ) : (
          <ChevronRightIcon className="h-5 w-5 text-gray-400" />
        )}
      </button>
      <div className="border-t border-gray-100 px-4 py-4">
        <p className="text-sm text-gray-700">{row.description}</p>
        {open && row.output && (
          <pre className="mt-3 rounded bg-gray-50 p-3 text-xs overflow-x-auto">
            {JSON.stringify(row.output, null, 2)}
          </pre>
        )}
      </div>
    </div>
  );
}