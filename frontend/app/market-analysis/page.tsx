"use client";

import { useState, type ElementType } from "react";
import {
  ArrowRight,
  BarChart3,
  Bot,
  BriefcaseBusiness,
  CheckCircle2,
  Copy,
  Database,
  Loader2,
  PackageCheck,
  Rocket,
  Search,
  ShieldAlert,
  Sparkles,
  Store,
  Target,
  TrendingUp,
} from "lucide-react";

import { api } from "@/lib/api";

type MarketResult = {
  matched_category: string;
  market_summary: string;
  demand_level: string;
  competition_level: string;
  recommended_products: string[];
  digital_product_ideas: string[];
  affiliate_product_ideas: string[];
  dropshipping_product_ideas: string[];
  best_platforms: string[];
  risk_level: string;
  opportunity_score: number;
  business_type_note: string;
  next_best_action: string;
  data_note: string;
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

export default function MarketAnalysisPage() {
  const [form, setForm] = useState({
    niche: "Personal finance",
    audience: "USA young professionals, age 22-35",
    region: "United States",
    platforms: ["TikTok", "Instagram Reels", "YouTube Shorts"],
    business_type: "Digital product + affiliate marketing",
    budget: "Low",
    product_interest:
      "Budget planner, finance template, creator-friendly digital product",
  });

  const [result, setResult] = useState<MarketResult | null>(null);
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

  async function handleAnalyze() {
    try {
      setLoading(true);
      setError("");
      setResult(null);

      const response = await api.post("/market/analyze", form);
      setResult(response.data);
    } catch {
      setError(
        "Backend connection failed. Make sure FastAPI is running on http://localhost:8000",
      );
    } finally {
      setLoading(false);
    }
  }

  async function copyText(text: string) {
    await navigator.clipboard.writeText(text);
  }

  return (
    <main className="min-h-screen bg-[#030816] px-5 py-8 text-white md:px-10">
      <div className="mx-auto max-w-7xl">
        <header className="mb-8 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
          <div>
            <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-orange-500/30 bg-orange-500/10 px-4 py-2 text-sm font-bold text-orange-200">
              <BarChart3 size={16} />
              AI Market Analysis
            </div>

            <h1 className="text-4xl font-black tracking-tight md:text-5xl">
              Find product opportunities for your creator niche.
            </h1>

            <p className="mt-3 max-w-3xl text-slate-400">
              Analyze your niche, audience, platform, and business interest to
              discover digital products, affiliate offers, and dropshipping
              opportunities.
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
                <Search size={22} />
              </div>

              <div>
                <h2 className="text-xl font-black">Market Input</h2>
                <p className="text-sm text-slate-400">
                  Give AI your niche, audience, region, and business direction.
                </p>
              </div>
            </div>

            <div className="grid gap-5">
              <Input
                label="Creator Niche"
                value={form.niche}
                onChange={(value) => updateField("niche", value)}
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
                label="Business Type"
                value={form.business_type}
                onChange={(value) => updateField("business_type", value)}
                placeholder="Digital product + affiliate marketing"
              />

              <Input
                label="Budget"
                value={form.budget}
                onChange={(value) => updateField("budget", value)}
                placeholder="Low"
              />

              <Textarea
                label="Product Interest"
                value={form.product_interest}
                onChange={(value) => updateField("product_interest", value)}
                placeholder="Budget planner, finance template, digital product..."
              />

              {error && (
                <div className="rounded-2xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-200">
                  {error}
                </div>
              )}

              <button
                onClick={handleAnalyze}
                disabled={loading}
                className="mt-2 flex items-center justify-center gap-3 rounded-2xl bg-gradient-to-r from-orange-500 via-fuchsia-500 to-violet-600 px-6 py-4 font-black text-white shadow-[0_0_30px_rgba(249,115,22,0.3)] disabled:cursor-not-allowed disabled:opacity-60"
              >
                {loading ? (
                  <>
                    <Loader2 className="animate-spin" size={20} />
                    Analyzing Market...
                  </>
                ) : (
                  <>
                    Analyze Market Opportunity
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
                  Your market opportunity report will appear here.
                </h2>

                <p className="mt-3 text-slate-400">
                  Run the analysis to discover product ideas, demand signals,
                  competition level, and next actions.
                </p>
              </div>
            ) : (
              <>
                <div className="rounded-3xl border border-orange-500/30 bg-gradient-to-br from-orange-950/70 to-slate-950 p-6 shadow-[0_0_50px_rgba(249,115,22,0.18)]">
                  <div className="flex items-center justify-between gap-4">
                    <div>
                      <p className="text-sm font-bold uppercase tracking-[0.2em] text-orange-300">
                        Opportunity Score
                      </p>

                      <h2 className="mt-2 text-5xl font-black">
                        {result.opportunity_score}
                        <span className="text-xl text-slate-400">/100</span>
                      </h2>

                      <p className="mt-2 text-slate-300">
                        Matched Category: {result.matched_category}
                      </p>
                    </div>

                    <div className="flex h-24 w-24 items-center justify-center rounded-full bg-gradient-to-br from-orange-500 to-fuchsia-500">
                      <TrendingUp size={42} />
                    </div>
                  </div>
                </div>

                <SingleResult
                  icon={Target}
                  title="Market Summary"
                  text={result.market_summary}
                  onCopy={copyText}
                />

                <div className="grid gap-4 md:grid-cols-3">
                  <MiniMetric
                    title="Demand Level"
                    value={result.demand_level}
                    icon={TrendingUp}
                    color="text-emerald-300"
                  />

                  <MiniMetric
                    title="Competition"
                    value={result.competition_level}
                    icon={ShieldAlert}
                    color="text-orange-300"
                  />

                  <MiniMetric
                    title="Risk Level"
                    value={result.risk_level}
                    icon={ShieldAlert}
                    color="text-pink-300"
                  />
                </div>

                <ResultSection
                  icon={PackageCheck}
                  title="Recommended Products"
                  items={result.recommended_products}
                  onCopy={copyText}
                />

                <ResultSection
                  icon={Sparkles}
                  title="Digital Product Ideas"
                  items={result.digital_product_ideas}
                  onCopy={copyText}
                />

                <ResultSection
                  icon={BriefcaseBusiness}
                  title="Affiliate Product Ideas"
                  items={result.affiliate_product_ideas}
                  onCopy={copyText}
                />

                <ResultSection
                  icon={Store}
                  title="Dropshipping Product Ideas"
                  items={result.dropshipping_product_ideas}
                  onCopy={copyText}
                />

                <ResultSection
                  icon={CheckCircle2}
                  title="Best Platforms"
                  items={result.best_platforms}
                  onCopy={copyText}
                />

                <SingleResult
                  icon={Rocket}
                  title="Business Type Note"
                  text={result.business_type_note}
                  onCopy={copyText}
                />

                <SingleResult
                  icon={ArrowRight}
                  title="Next Best Action"
                  text={result.next_best_action}
                  onCopy={copyText}
                />

                <div className="rounded-3xl border border-violet-500/30 bg-violet-500/10 p-5 text-sm leading-6 text-violet-100">
                  <div className="mb-2 flex items-center gap-2 font-black">
                    <Database size={18} />
                    MVP Data Note
                  </div>
                  {result.data_note}
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

function Textarea({
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

      <textarea
        value={value}
        onChange={(event) => onChange(event.target.value)}
        placeholder={placeholder}
        rows={4}
        className="w-full resize-none rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-white outline-none placeholder:text-slate-500 focus:border-orange-500/60"
      />
    </div>
  );
}

function SingleResult({
  icon: Icon,
  title,
  text,
  onCopy,
}: {
  icon: ElementType;
  title: string;
  text: string;
  onCopy: (text: string) => void;
}) {
  return (
    <div className="rounded-3xl border border-white/10 bg-[#0c1428] p-6">
      <div className="mb-3 flex items-center justify-between gap-4">
        <h3 className="flex items-center gap-2 text-xl font-black">
          <Icon className="text-orange-300" />
          {title}
        </h3>

        <button
          onClick={() => onCopy(text)}
          className="rounded-lg border border-white/10 bg-white/5 p-2 text-slate-300 hover:bg-white/10"
          title="Copy text"
        >
          <Copy size={16} />
        </button>
      </div>

      <p className="leading-7 text-slate-300">{text}</p>
    </div>
  );
}

function ResultSection({
  icon: Icon,
  title,
  items,
  onCopy,
}: {
  icon: ElementType;
  title: string;
  items: string[];
  onCopy: (text: string) => void;
}) {
  return (
    <div className="rounded-3xl border border-white/10 bg-[#0c1428] p-6">
      <div className="mb-4 flex items-center justify-between gap-4">
        <h3 className="flex items-center gap-2 text-xl font-black">
          <Icon className="text-fuchsia-300" />
          {title}
        </h3>

        <button
          onClick={() => onCopy(items.join("\n"))}
          className="rounded-lg border border-white/10 bg-white/5 p-2 text-slate-300 hover:bg-white/10"
          title="Copy all"
        >
          <Copy size={16} />
        </button>
      </div>

      <div className="grid gap-3">
        {items.map((item) => (
          <div
            key={item}
            className="rounded-xl border border-white/10 bg-white/5 p-4 text-sm font-semibold text-slate-200"
          >
            {item}
          </div>
        ))}
      </div>
    </div>
  );
}

function MiniMetric({
  title,
  value,
  icon: Icon,
  color,
}: {
  title: string;
  value: string;
  icon: ElementType;
  color: string;
}) {
  return (
    <div className="rounded-3xl border border-white/10 bg-[#0c1428] p-5">
      <div
        className={`mb-3 flex h-11 w-11 items-center justify-center rounded-2xl bg-white/10 ${color}`}
      >
        <Icon size={22} />
      </div>

      <p className="text-sm text-slate-400">{title}</p>
      <p className={`mt-1 text-2xl font-black ${color}`}>{value}</p>
    </div>
  );
}


