"use client";

import { useState, type ElementType } from "react";
import {
  ArrowRight,
  Bot,
  BriefcaseBusiness,
  CheckCircle2,
  Copy,
  Loader2,
  Megaphone,
  PackageCheck,
  Rocket,
  ShieldCheck,
  ShoppingBag,
  Sparkles,
  Store,
  Target,
  Truck,
} from "lucide-react";

import { api } from "@/lib/api";

type AffiliateRoadmapResult = {
  roadmap_summary: string;
  affiliate_product_ideas: string[];
  dropshipping_product_ideas: string[];
  best_product_fit: string;
  content_promotion_plan: string[];
  supplier_research_checklist: string[];
  thirty_day_roadmap: string[];
  risk_analysis: string[];
  ethical_disclosure: string;
  next_best_action: string;
  data_note: string;
};

const platformOptions = [
  "TikTok",
  "Instagram Reels",
  "YouTube Shorts",
  "YouTube Long-form",
  "Pinterest",
  "Newsletter",
  "Blog",
];

export default function AffiliateRoadmapPage() {
  const [form, setForm] = useState({
    niche: "Personal finance",
    audience: "USA young professionals, age 22-35",
    region: "United States",
    platforms: ["TikTok", "Instagram Reels", "YouTube Shorts"],
    business_type: "Affiliate marketing + digital product",
    budget: "Low",
    product_category: "Budget planner and finance tools",
    content_style: "Educational short-form content",
  });

  const [result, setResult] = useState<AffiliateRoadmapResult | null>(null);
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

  async function handleGenerate() {
    try {
      setLoading(true);
      setError("");
      setResult(null);

      const response = await api.post("/affiliate/roadmap", form);
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
            <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-violet-500/30 bg-violet-500/10 px-4 py-2 text-sm font-bold text-violet-200">
              <BriefcaseBusiness size={16} />
              Affiliate & Dropshipping Roadmap
            </div>

            <h1 className="text-4xl font-black tracking-tight md:text-5xl">
              Turn your content into product income.
            </h1>

            <p className="mt-3 max-w-3xl text-slate-400">
              Get affiliate product ideas, dropshipping opportunities, content
              promotion strategy, supplier checklist, risk analysis, and a
              30-day roadmap.
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
          <section className="rounded-3xl border border-white/10 bg-[#0c1428] p-6 shadow-[0_0_50px_rgba(168,85,247,0.12)]">
            <div className="mb-6 flex items-center gap-3">
              <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-to-br from-violet-600 to-orange-500">
                <ShoppingBag size={22} />
              </div>

              <div>
                <h2 className="text-xl font-black">Business Input</h2>
                <p className="text-sm text-slate-400">
                  Tell AI your niche, audience, product category, and content
                  style.
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
                          ? "border-violet-500/60 bg-violet-500/20 text-white"
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
                placeholder="Affiliate marketing + digital product"
              />

              <Input
                label="Budget"
                value={form.budget}
                onChange={(value) => updateField("budget", value)}
                placeholder="Low"
              />

              <Input
                label="Product Category"
                value={form.product_category}
                onChange={(value) => updateField("product_category", value)}
                placeholder="Budget planner and finance tools"
              />

              <Input
                label="Content Style"
                value={form.content_style}
                onChange={(value) => updateField("content_style", value)}
                placeholder="Educational short-form content"
              />

              {error && (
                <div className="rounded-2xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-200">
                  {error}
                </div>
              )}

              <button
                onClick={handleGenerate}
                disabled={loading}
                className="mt-2 flex items-center justify-center gap-3 rounded-2xl bg-gradient-to-r from-violet-600 via-fuchsia-500 to-orange-500 px-6 py-4 font-black text-white shadow-[0_0_30px_rgba(168,85,247,0.32)] disabled:cursor-not-allowed disabled:opacity-60"
              >
                {loading ? (
                  <>
                    <Loader2 className="animate-spin" size={20} />
                    Building Roadmap...
                  </>
                ) : (
                  <>
                    Generate Business Roadmap
                    <ArrowRight size={20} />
                  </>
                )}
              </button>
            </div>
          </section>

          <section className="space-y-5">
            {!result ? (
              <div className="rounded-3xl border border-white/10 bg-[#0c1428] p-8 text-center">
                <div className="mx-auto mb-5 flex h-20 w-20 items-center justify-center rounded-3xl bg-violet-500/20 text-violet-300">
                  <Bot size={38} />
                </div>

                <h2 className="text-2xl font-black">
                  Your affiliate and dropshipping roadmap will appear here.
                </h2>

                <p className="mt-3 text-slate-400">
                  Generate a content-led business plan before spending money on
                  products, ads, or store setup.
                </p>
              </div>
            ) : (
              <>
                <div className="rounded-3xl border border-violet-500/30 bg-gradient-to-br from-violet-950/70 to-slate-950 p-6 shadow-[0_0_50px_rgba(168,85,247,0.18)]">
                  <div className="flex items-center justify-between gap-4">
                    <div>
                      <p className="text-sm font-bold uppercase tracking-[0.2em] text-violet-300">
                        Content-to-Business Roadmap
                      </p>

                      <h2 className="mt-2 text-3xl font-black">
                        Affiliate & Dropshipping Plan
                      </h2>

                      <p className="mt-2 text-slate-300">
                        Built for validation-first creator monetization.
                      </p>
                    </div>

                    <div className="flex h-24 w-24 items-center justify-center rounded-full bg-gradient-to-br from-violet-600 to-orange-500">
                      <Rocket size={42} />
                    </div>
                  </div>
                </div>

                <SingleResult
                  icon={Target}
                  title="Roadmap Summary"
                  text={result.roadmap_summary}
                  onCopy={copyText}
                />

                <ResultSection
                  icon={PackageCheck}
                  title="Affiliate Product Ideas"
                  items={result.affiliate_product_ideas}
                  onCopy={copyText}
                />

                <ResultSection
                  icon={Truck}
                  title="Dropshipping Product Ideas"
                  items={result.dropshipping_product_ideas}
                  onCopy={copyText}
                />

                <SingleResult
                  icon={Store}
                  title="Best Product Fit"
                  text={result.best_product_fit}
                  onCopy={copyText}
                />

                <ResultSection
                  icon={Megaphone}
                  title="Content Promotion Plan"
                  items={result.content_promotion_plan}
                  onCopy={copyText}
                />

                <ResultSection
                  icon={CheckCircle2}
                  title="Supplier / Research Checklist"
                  items={result.supplier_research_checklist}
                  onCopy={copyText}
                />

                <ResultSection
                  icon={Rocket}
                  title="30-Day Roadmap"
                  items={result.thirty_day_roadmap}
                  onCopy={copyText}
                />

                <ResultSection
                  icon={ShieldCheck}
                  title="Risk Analysis"
                  items={result.risk_analysis}
                  onCopy={copyText}
                />

                <SingleResult
                  icon={ShieldCheck}
                  title="Affiliate Disclosure Reminder"
                  text={result.ethical_disclosure}
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
        className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-white outline-none placeholder:text-slate-500 focus:border-violet-500/60"
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
          <Icon className="text-violet-300" />
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


