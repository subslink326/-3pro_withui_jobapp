import { useState } from "react";

export default function UploadForm({ onRun, loading }) {
  const [jobUrl, setJobUrl] = useState("");
  const [resumeFile, setResumeFile] = useState(null);

  const submit = (e) => {
    e.preventDefault();
    if (!jobUrl || !resumeFile) {
      alert("Please enter job URL and attach résumé.");
      return;
    }
    onRun(jobUrl, resumeFile);
  };

  return (
    <form
      onSubmit={submit}
      className="bg-white shadow-md rounded-md p-6 space-y-4 mb-8"
    >
      <div>
        <label className="block text-sm font-medium text-gray-700">
          Job posting URL
        </label>
        <input
          type="url"
          value={jobUrl}
          onChange={(e) => setJobUrl(e.target.value)}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          placeholder="https://boards.greenhouse.io/..."
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">
          Résumé (PDF/DOCX)
        </label>
        <input
          type="file"
          accept=".pdf,.doc,.docx"
          onChange={(e) => setResumeFile(e.target.files[0])}
          className="mt-1 block w-full text-sm text-gray-500"
          required
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50"
      >
        {loading ? "Running…" : "Run JobFlow"}
      </button>
    </form>
  );
}