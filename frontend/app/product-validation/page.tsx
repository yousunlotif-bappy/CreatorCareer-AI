"use client";

import { useState, type ElementType } from "react";
import {
  ArrowRight,
  BarChart3,
  Bot,
  CheckCircle2,
  ClipboardCheck,
  Copy,
  Gauge,
  Loader2,
  PackageCheck,
  Rocket,
  ShieldAlert,
  Sparkles,
  Target,
  TrendingUp,
  WalletCards,
} from "lucide-react";

import { api } from "@/lib/api";

type ProductValidationResult = {
  product_name: string;
  status: string;
  total_score: number;
  score_breakdown: {
    audience_fit_score: number;
    market_demand_score: number;
    competition_score: number;
    content_promotion_fit_score: number;
    profit_potential_score: number;
    ease_of_starting_score: number;
    total_score: number;
  };
  recommendation: string;
  strengths: string[];
  risks: string[];
  validation_checklist: string[];
  next_best_action: string;
  data_note: string;
};

export default function ProductValidationPage() {
  const [form, setForm] = useState({
    product_name: "Notion Budget Planner Template",
    niche: "Personal finance",
    audience: "USA young professionals, age 22-35",
    region: "United States",
    platform: "TikTok + Instagram Reels + YouTube Shorts",
    business_model: "Digital product + affiliate marketing",
    budget: "Low",
    product_type: "Digital template",
    promotion_style: "Educational short-form content",
  });

  const [result, setResult] = useState<ProductValidationResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function updateField(field: keyof typeof form, value: string) {
    setForm((previousForm) => ({
      ...previousForm,
      [field]: value,
    }));
  }

  async function handleValidate() {
    try {
      setLoading(true);
      setError("");
      setResult(null);

      const response = await api.post("/product/validate", form);
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
            <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-amber-500/30 bg-amber-500/10 px-4 py-2 text-sm font-bold text-amber-200">
              <ClipboardCheck size={16} />
              Product Validation Score
            </div>

            <h1 className="text-4xl font-black tracking-tight md:text-5xl">
              Validate product ideas before you build.
            </h1>

            <p className="mt-3 max-w-3xl text-slate-400">
              Score product ideas using audience fit, market demand,
              competition, content promotion fit, profit potential, and ease of
              starting.
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
          <section className="rounded-3xl border border-white/10 bg-[#0c1428] p-6 shadow-[0_0_50px_rgba(245,158,11,0.12)]">
            <div className="mb-6 flex items-center gap-3">
              <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-to-br from-amber-500 to-fuchsia-500">
                <PackageCheck size={22} />
              </div>

              <div>
                <h2 className="text-xl font-black">Product Input</h2>
                <p className="text-sm text-slate-400">
                  Give AI the product idea, niche, audience, and business
                  model.
                </p>
              </div>
            </div>

            <div className="grid gap-5">
              <Input
                label="Product Name"
                value={form.product_name}
                onChange={(value) => updateField("product_name", value)}
                placeholder="Notion Budget Planner Template"
              />

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

              <Input
                label="Platform"
                value={form.platform}
                onChange={(value) => updateField("platform", value)}
                placeholder="TikTok + Instagram Reels + YouTube Shorts"
              />

              <Input
                label="Business Model"
                value={form.business_model}
                onChange={(value) => updateField("business_model", value)}
                placeholder="Digital product + affiliate marketing"
              />

              <Input
                label="Budget"
                value={form.budget}
                onChange={(value) => updateField("budget", value)}
                placeholder="Low"
              />

              <Input
                label="Product Type"
                value={form.product_type}
                onChange={(value) => updateField("product_type", value)}
                placeholder="Digital template"
              />

              <Input
                label="Promotion Style"
                value={form.promotion_style}
                onChange={(value) => updateField("promotion_style", value)}
                placeholder="Educational short-form content"
              />

              {error && (
                <div className="rounded-2xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-200">
                  {error}
                </div>
              )}

              <button
                onClick={handleValidate}
                disabled={loading}
                className="mt-2 flex items-center justify-center gap-3 rounded-2xl bg-gradient-to-r from-amber-500 via-orange-500 to-fuchsia-500 px-6 py-4 font-black text-white shadow-[0_0_30px_rgba(245,158,11,0.3)] disabled:cursor-not-allowed disabled:opacity-60"
              >
                {loading ? (
                  <>
                    <Loader2 className="animate-spin" size={20} />
                    Validating Product...
                  </>
                ) : (
                  <>
                    Validate Product Idea
                    <ArrowRight size={20} />
                  </>
                )}
              </button>
            </div>
          </section>

          <section className="space-y-5">
            {!result ? (
              <div className="rounded-3xl border border-white/10 bg-[#0c1428] p-8 text-center">
                <div className="mx-auto mb-5 flex h-20 w-20 items-center justify-center rounded-3xl bg-amber-500/20 text-amber-300">
                  <Bot size={38} />
                </div>

                <h2 className="text-2xl font-black">
                  Your product validation score will appear here.
                </h2>

                <p className="mt-3 text-slate-400">
                  Run the validation to see score breakdown, risks, strengths,
                  checklist, and next action.
                </p>
              </div>
            ) : (
              <>
                <div className="rounded-3xl border border-amber-500/30 bg-gradient-to-br from-amber-950/70 to-slate-950 p-6 shadow-[0_0_50px_rgba(245,158,11,0.18)]">
                  <div className="flex items-center justify-between gap-4">
                    <div>
                      <p className="text-sm font-bold uppercase tracking-[0.2em] text-amber-300">
                        Product Validation Score
                      </p>

                      <h2 className="mt-2 text-5xl font-black">
                        {result.total_score}
                        <span className="text-xl text-slate-400">/100</span>
                      </h2>

                      <p className="mt-2 text-slate-300">{result.status}</p>
                    </div>

                    <div className="flex h-24 w-24 items-center justify-center rounded-full bg-gradient-to-br from-amber-500 to-fuchsia-500">
                      <Gauge size={42} />
                    </div>
                  </div>
                </div>

                <SingleResult
                  icon={Target}
                  title="Recommendation"
                  text={result.recommendation}
                  onCopy={copyText}
                />

                <div className="grid gap-4 md:grid-cols-2">
                  <ScoreBox
                    title="Audience Fit"
                    score={result.score_breakdown.audience_fit_score}
                    max={25}
                    icon={Target}
                    color="text-violet-300"
                  />

                  <ScoreBox
                    title="Market Demand"
                    score={result.score_breakdown.market_demand_score}
                    max={20}
                    icon={TrendingUp}
                    color="text-emerald-300"
                  />

                  <ScoreBox
                    title="Competition"
                    score={result.score_breakdown.competition_score}
                    max={15}
                    icon={ShieldAlert}
                    color="text-orange-300"
                  />

                  <ScoreBox
                    title="Content Promotion Fit"
                    score={result.score_breakdown.content_promotion_fit_score}
                    max={20}
                    icon={BarChart3}
                    color="text-fuchsia-300"
                  />

                  <ScoreBox
                    title="Profit Potential"
                    score={result.score_breakdown.profit_potential_score}
                    max={10}
                    icon={WalletCards}
                    color="text-amber-300"
                  />

                  <ScoreBox
                    title="Ease of Starting"
                    score={result.score_breakdown.ease_of_starting_score}
                    max={10}
                    icon={Rocket}
                    color="text-sky-300"
                  />
                </div>

                <ResultSection
                  icon={CheckCircle2}
                  title="Strengths"
                  items={result.strengths}
                  onCopy={copyText}
                />

                <ResultSection
                  icon={ShieldAlert}
                  title="Risks"
                  items={result.risks}
                  onCopy={copyText}
                />

                <ResultSection
                  icon={ClipboardCheck}
                  title="Validation Checklist"
                  items={result.validation_checklist}
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
                    <Sparkles size={18} />
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
        className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-white outline-none placeholder:text-slate-500 focus:border-amber-500/60"
      />
    </div>
  );
}

function ScoreBox({
  title,
  score,
  max,
  icon: Icon,
  color,
}: {
  title: string;
  score: number;
  max: number;
  icon: ElementType;
  color: string;
}) {
  const percent = Math.round((score / max) * 100);

  return (
    <div className="rounded-3xl border border-white/10 bg-[#0c1428] p-5">
      <div
        className={`mb-3 flex h-11 w-11 items-center justify-center rounded-2xl bg-white/10 ${color}`}
      >
        <Icon size={22} />
      </div>

      <div className="mb-2 flex items-center justify-between">
        <p className="text-sm text-slate-400">{title}</p>
        <p className={`font-black ${color}`}>
          {score}/{max}
        </p>
      </div>

      <div className="h-2 overflow-hidden rounded-full bg-white/10">
        <div
          className="h-full rounded-full bg-gradient-to-r from-amber-400 to-fuchsia-500"
          style={{ width: `${percent}%` }}
        />
      </div>
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
          <Icon className="text-amber-300" />
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


