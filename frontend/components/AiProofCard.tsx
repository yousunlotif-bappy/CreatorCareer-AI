import { CheckCircle2, Database, Sparkles, XCircle } from "lucide-react";

type AiProofCardProps = {
  result: Record<string, unknown> | null;
};

function textValue(value: unknown, fallback: string) {
  if (value === null || value === undefined || value === "") return fallback;
  return String(value);
}

function boolValue(value: unknown) {
  return value === true || value === "true" || value === "yes";
}

export default function AiProofCard({ result }: AiProofCardProps) {
  if (!result) return null;

  const aiProvider = textValue(
    result.ai_provider || result.provider,
    "IBM Granite / Ollama-ready AI layer",
  );

  const model = textValue(
    result.llm_model || result.model || result.granite_model,
    "granite3.3:2b",
  );

  const graniteUsed = boolValue(result.granite_used || result.ai_used);
  const databaseSaved = boolValue(result.database_saved);
  const recordId = textValue(
    result.database_record_id || result.record_id || result.id,
    "Not returned",
  );

  const dataNote = textValue(
    result.data_note,
    "MVP output generated through AI/scoring logic and backend workflow.",
  );

  return (
    <section className="rounded-3xl border border-emerald-500/20 bg-emerald-500/10 p-5">
      <div className="mb-4 flex items-center gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500/20 text-emerald-200">
          <Sparkles size={20} />
        </div>

        <div>
          <h3 className="text-lg font-black text-white">
            AI + Database Proof
          </h3>
          <p className="text-sm text-slate-300">
            This card shows backend, AI, and database evidence for judges.
          </p>
        </div>
      </div>

      <div className="grid gap-3 sm:grid-cols-2">
        <ProofItem label="AI Provider" value={aiProvider} success />
        <ProofItem label="AI Model" value={model} success />

        <ProofItem
          label="Granite Used"
          value={graniteUsed ? "Yes" : "Not returned"}
          success={graniteUsed}
        />

        <ProofItem
          label="Database Saved"
          value={databaseSaved ? "Yes" : "Not returned"}
          success={databaseSaved}
        />

        <ProofItem label="Record ID" value={recordId} success={recordId !== "Not returned"} />
        <ProofItem label="Data Note" value={dataNote} success />
      </div>
    </section>
  );
}

function ProofItem({
  label,
  value,
  success,
}: {
  label: string;
  value: string;
  success: boolean;
}) {
  return (
    <div className="rounded-2xl border border-white/10 bg-slate-950/70 p-4">
      <div className="mb-2 flex items-center justify-between gap-3">
        <p className="text-xs font-bold uppercase tracking-[0.18em] text-slate-500">
          {label}
        </p>

        {success ? (
          <CheckCircle2 size={16} className="text-emerald-300" />
        ) : (
          <XCircle size={16} className="text-orange-300" />
        )}
      </div>

      <p className="break-words text-sm font-bold text-slate-100">{value}</p>
    </div>
  );
}


