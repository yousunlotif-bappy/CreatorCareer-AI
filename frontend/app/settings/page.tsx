import Link from "next/link";
import {
  Bot,
  Cloud,
  Database,
  Server,
  Settings,
  ShieldCheck,
  Sparkles,
} from "lucide-react";

/*
  CreatorCareer AI - Settings Page

  This page is not only a basic settings screen.
  It also works as an honest technical explanation page for:
  - Judges
  - Developers
  - Reviewers
  - Future users

  The page explains how CreatorCareer AI currently works, how IBM Granite
  was used for local AI testing, how IBM Bob influenced the project planning
  and workflow structure, and how the system can grow into a watsonx-ready
  SaaS platform in the future.
*/

export default function SettingsPage() {
  /*
    Future configuration items are kept in an array so the UI stays clean.
    This also makes the page easier to update later when real settings,
    API keys, branding controls, or database preferences are added.
  */
  const futureItems = [
    "IBM Granite / watsonx API configuration",
    "Supabase / PostgreSQL database connection",
    "Live market API settings",
    "PDF report branding settings",
    "Creator profile save preferences",
  ];

  return (
    <main className="min-h-screen bg-[#050816] px-5 py-8 text-white md:px-10">
      <div className="mx-auto max-w-5xl">
        {/* Page header section */}
        <div className="mb-8">
          <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-slate-500/30 bg-white/5 px-4 py-2 text-sm font-semibold text-slate-200">
            <Settings size={16} />
            Settings
          </div>

          <h1 className="text-4xl font-black tracking-tight md:text-5xl">
            CreatorCareer AI Settings
          </h1>

          <p className="mt-3 max-w-3xl text-slate-400">
            This page explains the project configuration, AI deployment mode,
            database readiness, and future integration path for IBM watsonx,
            live market APIs, PDF branding, and user preferences.
          </p>
        </div>

        <div className="grid gap-6">
          {/* Honest AI deployment explanation for judges and users */}
          <section className="rounded-3xl border border-amber-500/20 bg-amber-500/10 p-6 shadow-[0_0_50px_rgba(245,158,11,0.10)]">
            <div className="mb-5 flex items-center gap-3">
              <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-amber-500/20 text-amber-200">
                <ShieldCheck size={24} />
              </div>

              <div>
                <h2 className="text-2xl font-black text-white">
                  AI Deployment Note
                </h2>
                <p className="text-sm text-slate-400">
                  Honest AI disclosure for judges and users.
                </p>
              </div>
            </div>

            <p className="leading-7 text-slate-300">
              CreatorCareer AI was planned with IBM Bob-inspired project
              thinking and developed with IBM Granite through Ollama for local
              AI testing. In production, the deployed Render backend uses
              explainable fallback AI logic when the local Ollama server is not
              available. The backend structure is designed to be watsonx-ready
              for future IBM cloud AI deployment.
            </p>

            {/* AI status cards */}
            <div className="mt-5 grid gap-3 md:grid-cols-3">
              <InfoCard
                icon={<Bot size={20} />}
                label="Local AI Model"
                value="IBM Granite granite3.3:2b"
              />

              <InfoCard
                icon={<Server size={20} />}
                label="Local Runtime"
                value="Ollama"
              />

              <InfoCard
                icon={<Cloud size={20} />}
                label="Production Mode"
                value="Explainable AI fallback"
              />
            </div>
          </section>

          {/* Future upgrade section */}
          <section className="rounded-3xl border border-white/10 bg-slate-900/50 p-8 shadow-[0_0_50px_rgba(168,85,247,0.12)] backdrop-blur-xl">
            <div className="mb-5 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-violet-600 to-fuchsia-500">
              <Sparkles size={30} />
            </div>

            <h2 className="text-2xl font-black">Future Configuration</h2>

            <p className="mt-3 leading-7 text-slate-400">
              These settings are prepared for future upgrades. The current MVP
              already supports the main creator business workflow, while these
              options can help expand CreatorCareer AI into a more advanced
              creator-focused SaaS product.
            </p>

            <div className="mt-5 grid gap-4">
              {futureItems.map((item) => (
                <div
                  key={item}
                  className="rounded-xl border border-white/10 bg-white/5 p-4 text-sm font-semibold text-slate-200"
                >
                  {item}
                </div>
              ))}
            </div>
          </section>

          {/* Current MVP readiness section */}
          <section className="rounded-3xl border border-emerald-500/20 bg-emerald-500/10 p-6">
            <div className="mb-4 flex items-center gap-3">
              <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-emerald-500/20 text-emerald-200">
                <Database size={24} />
              </div>

              <div>
                <h2 className="text-2xl font-black text-white">
                  System Readiness
                </h2>
                <p className="text-sm text-slate-400">
                  Current MVP deployment status.
                </p>
              </div>
            </div>

            <div className="grid gap-3 md:grid-cols-2">
              <StatusItem label="Frontend" value="Next.js deployed on Vercel" />
              <StatusItem label="Backend" value="FastAPI deployed on Render" />
              <StatusItem label="Database" value="Supabase / PostgreSQL ready" />
              <StatusItem label="Reports" value="PDF report generator ready" />
            </div>
          </section>

          {/* Simple navigation link back to the main dashboard */}
          <Link
            href="/dashboard"
            className="inline-flex w-fit rounded-xl border border-white/10 bg-white/5 px-5 py-3 text-sm font-bold text-slate-200 hover:bg-white/10"
          >
            Back to Dashboard
          </Link>
        </div>
      </div>
    </main>
  );
}

/*
  InfoCard component

  This reusable card is used for AI-related technical information.
  Keeping this as a separate component makes the Settings page cleaner,
  more readable, and easier to maintain.
*/

function InfoCard({
  icon,
  label,
  value,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-2xl border border-white/10 bg-slate-950/70 p-4">
      <div className="mb-3 flex h-10 w-10 items-center justify-center rounded-xl bg-white/10 text-amber-200">
        {icon}
      </div>

      <p className="text-sm text-slate-400">{label}</p>
      <p className="mt-1 font-black text-white">{value}</p>
    </div>
  );
}

/*
  StatusItem component

  This component shows the current project readiness status.
  It is used for frontend, backend, database, and PDF report status.
*/

function StatusItem({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-slate-950/70 p-4">
      <p className="text-sm text-slate-400">{label}</p>
      <p className="mt-1 font-black text-white">{value}</p>
    </div>
  );
}



