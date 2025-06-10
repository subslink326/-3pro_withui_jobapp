import { useState } from "react";
import UploadForm from "./components/UploadForm";
import WorkflowTable from "./components/WorkflowTable";

export default function App() {
  const [table, setTable] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleRun = async (jobUrl, resumeFile) => {
    setLoading(true);
    const form = new FormData();
    form.append("job_url", jobUrl);
    form.append("resume", resumeFile);

    try {
      const resp = await fetch("http://localhost:8000/run", {
        method: "POST",
        body: form,
      });
      if (!resp.ok) throw new Error(await resp.text());
      const data = await resp.json();
      setTable(data.table);
    } catch (err) {
      alert(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full">
      <header className="bg-white shadow-sm">
        <div className="mx-auto max-w-6xl px-4 py-4 flex items-center justify-between">
          <h1 className="text-xl font-semibold tracking-tight text-indigo-600">
            JobFlow Web
          </h1>
          <a
            href="https://github.com/your-org/jobflow-web"
            className="text-xs text-gray-500 hover:text-indigo-500"
          >
            GitHub ↗
          </a>
        </div>
      </header>

      <main className="flex-1 overflow-y-auto">
        <div className="mx-auto max-w-5xl p-6">
          <UploadForm onRun={handleRun} loading={loading} />
          {table && <WorkflowTable rows={table} />}
        </div>
      </main>

      <footer className="py-4 text-center text-xs text-gray-400">
        © 2025 JobFlow Project
      </footer>
    </div>
  );
}