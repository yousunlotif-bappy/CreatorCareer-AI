import Link from "next/link";
import { Settings, Sparkles } from "lucide-react";

export default function SettingsPage() {
  return (
    <main className="min-h-screen bg-[#050816] px-5 py-8 text-white md:px-10">
      <div className="mx-auto max-w-5xl">
        <div className="mb-8">
          <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-slate-500/30 bg-white/5 px-4 py-2 text-sm font-semibold text-slate-200">
            <Settings size={16} />
            Settings
          </div>

          <h1 className="text-4xl font-black tracking-tight md:text-5xl">
            CreatorCareer AI Settings
          </h1>

          <p className="mt-3 max-w-3xl text-slate-400">
            This page is prepared for future integrations like IBM
            Granite/watsonx API keys, Supabase database, live market APIs, PDF
            branding, and user preferences.
          </p>
        </div>

        <section className="rounded-3xl border border-white/10 bg-slate-900/50 p-8 shadow-[0_0_50px_rgba(168,85,247,0.12)] backdrop-blur-xl">
          <div className="mb-5 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-violet-600 to-fuchsia-500">
            <Sparkles size={30} />
          </div>

          <h2 className="text-2xl font-black">Future Configuration</h2>

          <div className="mt-5 grid gap-4">
            {[
              "IBM Granite / watsonx API configuration",
              "Supabase / PostgreSQL database connection",
              "Live market API settings",
              "PDF report branding settings",
              "Creator profile save preferences",
            ].map((item) => (
              <div
                key={item}
                className="rounded-xl border border-white/10 bg-white/5 p-4 text-sm font-semibold text-slate-200"
              >
                {item}
              </div>
            ))}
          </div>

          <Link
            href="/dashboard"
            className="mt-8 inline-flex rounded-xl border border-white/10 bg-white/5 px-5 py-3 text-sm font-bold text-slate-200 hover:bg-white/10"
          >
            Back to Dashboard
          </Link>
        </section>
      </div>
    </main>
  );
}


