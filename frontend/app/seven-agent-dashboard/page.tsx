"use client";

import { useState, type ElementType } from "react";
import {
  ArrowRight,
  Bot,
  BriefcaseBusiness,
  CalendarDays,
  Copy,
  Gauge,
  Loader2,
  PackageCheck,
  Rocket,
  ShieldCheck,
  Sparkles,
  Target,
  Users,
  WalletCards,
} from "lucide-react";

import { api } from "@/lib/api";

type AgentResult = {
  agent_name: string;
  score: number;
  status: string;
  reason: string;
  recommendation: string;
  next_action: string;
  roadmap_steps?: string[];
  issues_found?: string[];
  recommended_disclosure?: string;
  checklist?: string[];
  roadmap?: string[];
};

type SevenAgentResult = {
  overall_business_opportunity_score: number;
  executive_summary: string;
  agent_results: AgentResult[];
  next_7_days_plan: string[];
  score_weights: Record<string, string>;
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

const agentIcons: Record<string, ElementType> = {
  "Creator Business Readiness": Gauge,
  "Niche-to-Product Fit": Target,
  "Audience-to-Market Matching": Users,
  "Content-to-Commerce Roadmap": WalletCards,
  "Ethical Monetization Checker": ShieldCheck,
  "Product Validation Checklist": PackageCheck,
  "6-Month Creator-to-Business Roadmap": CalendarDays,
};

export default function SevenAgentDashboardPage() {
  const [form, setForm] = useState({
    creator_niche: "Personal finance",
    audience: "USA young professionals, age 22-35",
    region: "United States",
    platforms: ["TikTok", "Instagram Reels", "YouTube Shorts"],
    followers: 25000,
    product_idea: "Notion Budget Planner Template",
    business_model: "Digital product + affiliate marketing",
    income_goal: "$2,000/month in 6 months",
    available_time: "2 hours/day",
    promotion_copy:
      "This content may contain affiliate links. This budget planner may help you organize spending and build better money habits.",
  });

  const [result, setResult] = useState<SevenAgentResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function updateField(
    field: keyof typeof form,
    value: string | number | string[],
  ) {
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

  async function handleRunAgents() {
    try {
      setLoading(true);
      setError("");
      setResult(null);

      const response = await api.post("/agents/run", form);
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
            <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-fuchsia-500/30 bg-fuchsia-500/10 px-4 py-2 text-sm font-bold text-fuchsia-200">
              <Bot size={16} />
              7-Agent Creator Business Dashboard
            </div>

            <h1 className="text-4xl font-black tracking-tight md:text-5xl">
              Run seven AI agents in one business report.
            </h1>

            <p className="mt-3 max-w-3xl text-slate-400">
              Analyze creator readiness, product fit, market match, content
              roadmap, ethical monetization, product validation, and a 6-month
              growth plan.
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
          <section className="rounded-3xl border border-white/10 bg-[#0c1428] p-6 shadow-[0_0_50px_rgba(217,70,239,0.12)]">
            <div className="mb-6 flex items-center gap-3">
              <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-to-br from-fuchsia-500 to-orange-500">
                <Sparkles size={22} />
              </div>

              <div>
                <h2 className="text-xl font-black">Agent Input</h2>
                <p className="text-sm text-slate-400">
                  Give AI your creator profile, product idea, and goal.
                </p>
              </div>
            </div>

            <div className="grid gap-5">
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
                          ? "border-fuchsia-500/60 bg-fuchsia-500/20 text-white"
                          : "border-white/10 bg-white/5 text-slate-300 hover:bg-white/10"
                      }`}
                    >
                      {platform}
                    </button>
                  ))}
                </div>
              </div>

              <Input
                label="Follower Count"
                type="number"
                value={String(form.followers)}
                onChange={(value) => updateField("followers", Number(value))}
                placeholder="25000"
              />

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

              <Input
                label="Available Time"
                value={form.available_time}
                onChange={(value) => updateField("available_time", value)}
                placeholder="2 hours/day"
              />

              <Textarea
                label="Promotion Copy"
                value={form.promotion_copy}
                onChange={(value) => updateField("promotion_copy", value)}
                placeholder="Paste promotional copy with disclosure here..."
              />

              {error && (
                <div className="rounded-2xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-200">
                  {error}
                </div>
              )}

              <button
                onClick={handleRunAgents}
                disabled={loading}
                className="mt-2 flex items-center justify-center gap-3 rounded-2xl bg-gradient-to-r from-fuchsia-500 via-violet-600 to-orange-500 px-6 py-4 font-black text-white shadow-[0_0_30px_rgba(217,70,239,0.35)] disabled:cursor-not-allowed disabled:opacity-60"
              >
                {loading ? (
                  <>
                    <Loader2 className="animate-spin" size={20} />
                    Running 7 AI Agents...
                  </>
                ) : (
                  <>
                    Run 7-Agent Analysis
                    <ArrowRight size={20} />
                  </>
                )}
              </button>
            </div>
          </section>

          <section className="space-y-5">
            {!result ? (
              <div className="rounded-3xl border border-white/10 bg-[#0c1428] p-8 text-center">
                <div className="mx-auto mb-5 flex h-20 w-20 items-center justify-center rounded-3xl bg-fuchsia-500/20 text-fuchsia-300">
                  <Bot size={38} />
                </div>

                <h2 className="text-2xl font-black">
                  Your 7-agent business report will appear here.
                </h2>

                <p className="mt-3 text-slate-400">
                  Run the agents to generate scores, recommendations, roadmap,
                  checklist, and next 7 days plan.
                </p>
              </div>
            ) : (
              <>
                <div className="rounded-3xl border border-fuchsia-500/30 bg-gradient-to-br from-fuchsia-950/70 to-slate-950 p-6 shadow-[0_0_50px_rgba(217,70,239,0.18)]">
                  <div className="flex items-center justify-between gap-4">
                    <div>
                      <p className="text-sm font-bold uppercase tracking-[0.2em] text-fuchsia-300">
                        Overall Business Opportunity
                      </p>

                      <h2 className="mt-2 text-5xl font-black">
                        {result.overall_business_opportunity_score}
                        <span className="text-xl text-slate-400">/100</span>
                      </h2>

                      <p className="mt-2 text-slate-300">
                        Unified creator business intelligence score
                      </p>
                    </div>

                    <div className="flex h-24 w-24 items-center justify-center rounded-full bg-gradient-to-br from-fuchsia-500 to-orange-500">
                      <Rocket size={42} />
                    </div>
                  </div>
                </div>

                <SingleResult
                  icon={BriefcaseBusiness}
                  title="Executive Summary"
                  text={result.executive_summary}
                  onCopy={copyText}
                />

                <div className="grid gap-4">
                  {result.agent_results.map((agent) => (
                    <AgentCard
                      key={agent.agent_name}
                      agent={agent}
                      onCopy={copyText}
                    />
                  ))}
                </div>

                <ResultSection
                  icon={CalendarDays}
                  title="Next 7 Days Action Plan"
                  items={result.next_7_days_plan}
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
  type = "text",
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  placeholder: string;
  type?: string;
}) {
  return (
    <div>
      <label className="mb-2 block text-sm font-bold text-slate-200">
        {label}
      </label>

      <input
        type={type}
        value={value}
        onChange={(event) => onChange(event.target.value)}
        placeholder={placeholder}
        className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-white outline-none placeholder:text-slate-500 focus:border-fuchsia-500/60"
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
        rows={5}
        className="w-full resize-none rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-white outline-none placeholder:text-slate-500 focus:border-fuchsia-500/60"
      />
    </div>
  );
}

function AgentCard({
  agent,
  onCopy,
}: {
  agent: AgentResult;
  onCopy: (text: string) => void;
}) {
  const Icon = agentIcons[agent.agent_name] || Bot;

  const extraItems =
    agent.roadmap_steps ||
    agent.issues_found ||
    agent.checklist ||
    agent.roadmap ||
    [];

  const copyContent = [
    `${agent.agent_name}: ${agent.score}/100`,
    `Status: ${agent.status}`,
    `Reason: ${agent.reason}`,
    `Recommendation: ${agent.recommendation}`,
    `Next Action: ${agent.next_action}`,
    ...extraItems,
  ].join("\n");

  return (
    <div className="rounded-3xl border border-white/10 bg-[#0c1428] p-6">
      <div className="mb-5 flex items-start justify-between gap-4">
        <div className="flex gap-4">
          <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-fuchsia-500/30 to-orange-500/20 text-fuchsia-200">
            <Icon size={26} />
          </div>

          <div>
            <h3 className="text-xl font-black">{agent.agent_name}</h3>
            <p className="mt-1 text-sm text-slate-400">{agent.status}</p>
          </div>
        </div>

        <button
          onClick={() => onCopy(copyContent)}
          className="rounded-lg border border-white/10 bg-white/5 p-2 text-slate-300 hover:bg-white/10"
          title="Copy agent result"
        >
          <Copy size={16} />
        </button>
      </div>

      <div className="mb-5">
        <div className="mb-2 flex items-center justify-between">
          <span className="text-sm text-slate-400">Agent Score</span>
          <span className="text-xl font-black text-fuchsia-300">
            {agent.score}/100
          </span>
        </div>

        <div className="h-2 overflow-hidden rounded-full bg-white/10">
          <div
            className="h-full rounded-full bg-gradient-to-r from-fuchsia-500 to-orange-500"
            style={{ width: `${agent.score}%` }}
          />
        </div>
      </div>

      <div className="space-y-4">
        <TextBlock title="Reason" text={agent.reason} />
        <TextBlock title="Recommendation" text={agent.recommendation} />
        <TextBlock title="Next Action" text={agent.next_action} />

        {agent.recommended_disclosure && (
          <TextBlock
            title="Recommended Disclosure"
            text={agent.recommended_disclosure}
          />
        )}

        {extraItems.length > 0 && (
          <div>
            <h4 className="mb-3 font-black text-orange-300">Extra Output</h4>

            <div className="grid gap-3">
              {extraItems.map((item) => (
                <div
                  key={item}
                  className="rounded-xl border border-white/10 bg-white/5 p-4 text-sm font-semibold text-slate-200"
                >
                  {item}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function TextBlock({ title, text }: { title: string; text: string }) {
  return (
    <div>
      <h4 className="mb-1 font-black text-fuchsia-300">{title}</h4>
      <p className="leading-7 text-slate-300">{text}</p>
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
          <Icon className="text-fuchsia-300" />
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
          <Icon className="text-orange-300" />
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



