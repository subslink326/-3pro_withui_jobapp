import StepCard from "./StepCard";

export default function WorkflowTable({ rows }) {
  return (
    <div className="space-y-6">
      {rows.map((r) => (
        <StepCard key={r.step} row={r} />
      ))}
    </div>
  );
}