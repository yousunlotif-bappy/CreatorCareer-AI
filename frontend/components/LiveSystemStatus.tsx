"use client";

import { useEffect, useState } from "react";
import { Bot, CheckCircle2, Database, Loader2, RefreshCcw } from "lucide-react";

import { api } from "@/lib/api";

type StatusData = {
  aiHealth: Record<string, unknown> | null;
  dbHealth: Record<string, unknown> | null;
  dbOverview: Record<string, unknown> | null;
};

function readText(data: Record<string, unknown> | null, keys: string[], fallback: string) {
  if (!data) return fallback;

  for (const key of keys) {
    if (data[key] !== undefined && data[key] !== null) {
      return String(data[key]);
    }
  }

  return fallback;
}

function readBool(data: Record<string, unknown> | null, keys: string[]) {
  if (!data) return false;

  return keys.some((key) => {
    const value = data[key];
    return value === true || value === "true" || value === "ok" || value === "healthy";
  });
}

export default function LiveSystemStatus() {
  const [data, setData] = useState<StatusData>({
    aiHealth: null,
    dbHealth: null,
    dbOverview: null,
  });

  const [loading, setLoading] = useState(true);

  async function loadStatus() {
    setLoading(true);

    try {
      const [aiHealth, dbHealth, dbOverview] = await Promise.allSettled([
        api.get("/ai/health"),
        api.get("/db/health"),
        api.get("/db/overview"),
      ]);

      setData({
        aiHealth: aiHealth.status === "fulfilled" ? aiHealth.value.data : null,
        dbHealth: dbHealth.status === "fulfilled" ? dbHealth.value.data : null,
        dbOverview:
          dbOverview.status === "fulfilled" ? dbOverview.value.data : null,
      });
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadStatus();
  }, []);

  const aiActive =
    readBool(data.aiHealth, ["ollama_running", "model_available", "granite_available"]) ||
    readText(data.aiHealth, ["status"], "").toLowerCase().includes("ok");

  const dbActive =
    readBool(data.dbHealth, ["connected", "database_connected", "supabase_connected"]) ||
    readText(data.dbHealth, ["status"], "").toLowerCase().includes("ok");

  const modelName = readText(
    data.aiHealth,
    ["model", "model_name", "granite_model", "available_model"],
    "granite3.3:2b",
  );

  return (
    <section className="mt-6 rounded-3xl border border-emerald-500/20 bg-emerald-500/10 p-5">
      <div className="mb-5 flex items-center justify-between gap-4">
        <div>
          <h3 className="text-xl font-black text-white">
            Live System Proof
          </h3>
          <p className="text-sm text-slate-300">
            Real backend, AI, and Supabase status from FastAPI.
          </p>
        </div>

        <button
          onClick={loadStatus}
          className="flex items-center gap-2 rounded-xl border border-white/10 bg-white/5 px-4 py-2 text-sm font-bold text-white hover:bg-white/10"
        >
          {loading ? <Loader2 size={16} className="animate-spin" /> : <RefreshCcw size={16} />}
          Refresh
        </button>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <StatusCard
          icon={Bot}
          title="AI Service"
          value={aiActive ? "Active" : "Check Needed"}
          detail={`Model: ${modelName}`}
          success={aiActive}
        />

        <StatusCard
          icon={Database}
          title="Database"
          value={dbActive ? "Connected" : "Check Needed"}
          detail="Supabase / PostgreSQL"
          success={dbActive}
        />

        <StatusCard
          icon={CheckCircle2}
          title="Saved Records"
          value={data.dbOverview ? "Overview Loaded" : "No Overview"}
          detail="Reads /db/overview"
          success={Boolean(data.dbOverview)}
        />
      </div>

      {data.dbOverview && (
        <details className="mt-4 rounded-2xl border border-white/10 bg-slate-950/70 p-4">
          <summary className="cursor-pointer text-sm font-bold text-white">
            View database overview JSON
          </summary>

          <pre className="mt-4 max-h-52 overflow-auto text-xs leading-6 text-slate-300">
            {JSON.stringify(data.dbOverview, null, 2)}
          </pre>
        </details>
      )}
    </section>
  );
}

function StatusCard({
  icon: Icon,
  title,
  value,
  detail,
  success,
}: {
  icon: typeof Bot;
  title: string;
  value: string;
  detail: string;
  success: boolean;
}) {
  return (
    <div className="rounded-2xl border border-white/10 bg-slate-950/70 p-5">
      <div className="mb-4 flex items-center justify-between">
        <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-white/10 text-emerald-200">
          <Icon size={22} />
        </div>

        <span
          className={`rounded-full px-3 py-1 text-xs font-black ${
            success
              ? "bg-emerald-500/20 text-emerald-200"
              : "bg-orange-500/20 text-orange-200"
          }`}
        >
          {success ? "OK" : "CHECK"}
        </span>
      </div>

      <p className="text-sm text-slate-400">{title}</p>
      <h4 className="mt-1 text-2xl font-black text-white">{value}</h4>
      <p className="mt-2 text-sm text-slate-400">{detail}</p>
    </div>
  );
}


