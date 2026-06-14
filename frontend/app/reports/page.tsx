"use client";

import { useState } from "react";
import {
  ArrowRight,
  Bot,
  CheckCircle2,
  Download,
  FileText,
  Loader2,
  Sparkles,
} from "lucide-react";

import { api } from "@/lib/api";

type ReportResult = {
  status: string;
  message: string;
  file_name: string;
  download_url: string;
};

const platformOptions = [
  "TikTok",
  "Instagram Reels",
  "YouTube Shorts",
  "YouTube Long-form",
  "Pinterest",
  "LinkedIn",
  "Newsletter",
];

export default function ReportsPage() {
  const [form, setForm] = useState({
    creator_name: "Alex Morgan",
    creator_niche: "Personal finance",
    audience: "USA young professionals, age 22-35",
    region: "United States",
    platforms: ["TikTok", "Instagram Reels", "YouTube Shorts"],
    product_idea: "Notion Budget Planner Template",
    business_model: "Digital product + affiliate marketing",
    income_goal: "$2,000/month in 6 months",
  });

  const [result, setResult] = useState<ReportResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function updateField(field: keyof typeof form, value: string | string[]) {
    setForm((previousForm) => ({
      ...previousForm,
      [field]: value,
    }));
  }

  function togglePlatform(platform: string) {
    setForm((previousForm) => {
      const alreadySelected = previousForm.platforms.includes(platform);

      return {
        ...previousForm,
        platforms: alreadySelected
          ? previousForm.platforms.filter((item) => item !== platform)
          : [...previousForm.platforms, platform],
      };
    });
  }

  async function handleGenerateReport() {
    try {
      setLoading(true);
      setError("");
      setResult(null);

      const response = await api.post("/report/generate", form);
      setResult(response.data);
    } catch {
      setError(
        "Backend connection failed. Make sure FastAPI is running on http://localhost:8000",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-[#030816] px-5 py-8 text-white md:px-10">
      <div className="mx-auto max-w-7xl">
        <header className="mb-8 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
          <div>
            <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-orange-500/30 bg-orange-500/10 px-4 py-2 text-sm font-bold text-orange-200">
              <FileText size={16} />
              PDF Business Report
            </div>

            <h1 className="text-4xl font-black tracking-tight md:text-5xl">
              Download your creator business report.
            </h1>

            <p className="mt-3 max-w-3xl text-slate-400">
              Generate a PDF report with creator profile summary, scores,
              7-agent analysis, ethical note, next 7 days plan, and 6-month
              roadmap.
            </p>
          </div>

          <a
            href="/dashboard"
            className="rounded-xl border border-white/10 bg-white/5 px-5 py-3 text-sm font-bold text-slate-200 hover:bg-white/10"
          >
            Back to Dashboard
          </a>
        </header>

        <div className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
          <section className="rounded-3xl border border-white/10 bg-[#0c1428] p-6 shadow-[0_0_50px_rgba(249,115,22,0.12)]">
            <div className="mb-6 flex items-center gap-3">
              <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-to-br from-orange-500 to-fuchsia-500">
                <Sparkles size={22} />
              </div>

              <div>
                <h2 className="text-xl font-black">Report Input</h2>
                <p className="text-sm text-slate-400">
                  This information will be placed inside the PDF report.
                </p>
              </div>
            </div>

            <div className="grid gap-5">
              <Input
                label="Creator Name"
                value={form.creator_name}
                onChange={(value) => updateField("creator_name", value)}
                placeholder="Alex Morgan"
              />

              <Input
                label="Creator Niche"
                value={form.creator_niche}
                onChange={(value) => updateField("creator_niche", value)}
                placeholder="Personal finance"
              />

              <Input
                label="Target Audience"
                value={form.audience}
                onChange={(value) => updateField("audience", value)}
                placeholder="USA young professionals, age 22-35"
              />

              <Input
                label="Region"
                value={form.region}
                onChange={(value) => updateField("region", value)}
                placeholder="United States"
              />

              <div>
                <label className="mb-3 block text-sm font-bold text-slate-200">
                  Platforms
                </label>

                <div className="grid gap-3 sm:grid-cols-2">
                  {platformOptions.map((platform) => (
                    <button
                      key={platform}
                      type="button"
                      onClick={() => togglePlatform(platform)}
                      className={`rounded-xl border px-4 py-3 text-left text-sm font-semibold transition ${
                        form.platforms.includes(platform)
                          ? "border-orange-500/60 bg-orange-500/20 text-white"
                          : "border-white/10 bg-white/5 text-slate-300 hover:bg-white/10"
                      }`}
                    >
                      {platform}
                    </button>
                  ))}
                </div>
              </div>

              <Input
                label="Product Idea"
                value={form.product_idea}
                onChange={(value) => updateField("product_idea", value)}
                placeholder="Notion Budget Planner Template"
              />

              <Input
                label="Business Model"
                value={form.business_model}
                onChange={(value) => updateField("business_model", value)}
                placeholder="Digital product + affiliate marketing"
              />

              <Input
                label="Income Goal"
                value={form.income_goal}
                onChange={(value) => updateField("income_goal", value)}
                placeholder="$2,000/month in 6 months"
              />

              {error && (
                <div className="rounded-2xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-200">
                  {error}
                </div>
              )}

              <button
                onClick={handleGenerateReport}
                disabled={loading}
                className="mt-2 flex items-center justify-center gap-3 rounded-2xl bg-gradient-to-r from-orange-500 via-fuchsia-500 to-violet-600 px-6 py-4 font-black text-white shadow-[0_0_30px_rgba(249,115,22,0.3)] disabled:cursor-not-allowed disabled:opacity-60"
              >
                {loading ? (
                  <>
                    <Loader2 className="animate-spin" size={20} />
                    Generating PDF Report...
                  </>
                ) : (
                  <>
                    Generate PDF Report
                    <ArrowRight size={20} />
                  </>
                )}
              </button>
            </div>
          </section>

          <section className="space-y-5">
            {!result ? (
              <div className="rounded-3xl border border-white/10 bg-[#0c1428] p-8 text-center">
                <div className="mx-auto mb-5 flex h-20 w-20 items-center justify-center rounded-3xl bg-orange-500/20 text-orange-300">
                  <Bot size={38} />
                </div>

                <h2 className="text-2xl font-black">
                  Your downloadable PDF report will appear here.
                </h2>

                <p className="mt-3 text-slate-400">
                  Generate a full CreatorCareer AI report for demo and
                  submission.
                </p>
              </div>
            ) : (
              <>
                <div className="rounded-3xl border border-emerald-500/30 bg-gradient-to-br from-emerald-950/70 to-slate-950 p-8 shadow-[0_0_50px_rgba(16,185,129,0.18)]">
                  <div className="mb-5 flex h-20 w-20 items-center justify-center rounded-3xl bg-emerald-500/20 text-emerald-300">
                    <CheckCircle2 size={42} />
                  </div>

                  <p className="text-sm font-bold uppercase tracking-[0.2em] text-emerald-300">
                    Report Ready
                  </p>

                  <h2 className="mt-3 text-3xl font-black">
                    PDF generated successfully.
                  </h2>

                  <p className="mt-3 text-slate-300">{result.message}</p>

                  <p className="mt-4 rounded-xl border border-white/10 bg-white/5 p-4 text-sm text-slate-300">
                    File: {result.file_name}
                  </p>

                  <a
                    href={result.download_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="mt-6 inline-flex items-center gap-3 rounded-2xl bg-gradient-to-r from-emerald-500 via-fuchsia-500 to-orange-500 px-6 py-4 font-black text-white shadow-[0_0_30px_rgba(16,185,129,0.3)]"
                  >
                    Download PDF Report
                    <Download size={20} />
                  </a>
                </div>

                <div className="rounded-3xl border border-violet-500/30 bg-violet-500/10 p-5 text-sm leading-6 text-violet-100">
                  This generated report is perfect for your demo video. Show
                  the report generation and download button near the end of the
                  demo.
                </div>
              </>
            )}
          </section>
        </div>
      </div>
    </main>
  );
}

function Input({
  label,
  value,
  onChange,
  placeholder,
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  placeholder: string;
}) {
  return (
    <div>
      <label className="mb-2 block text-sm font-bold text-slate-200">
        {label}
      </label>

      <input
        value={value}
        onChange={(event) => onChange(event.target.value)}
        placeholder={placeholder}
        className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-white outline-none placeholder:text-slate-500 focus:border-orange-500/60"
      />
    </div>
  );
}


