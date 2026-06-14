"use client";

import { useState, type ElementType } from "react";
import {
  ArrowRight,
  Bot,
  BriefcaseBusiness,
  CheckCircle2,
  Clock,
  Loader2,
  Rocket,
  Sparkles,
  Target,
  User,
  Users,
} from "lucide-react";

import { api } from "@/lib/api";

type ProfileResult = {
  creator_summary: string;
  creator_stage: string;
  niche_positioning: string;
  audience_opportunity: string;
  business_opportunity: string;
  business_readiness_score: number;
  recommended_next_modules: string[];
  next_best_action: string;
};

const platformOptions = [
  "TikTok",
  "Instagram Reels",
  "YouTube Shorts",
  "YouTube Long-form",
  "Facebook Reels",
  "LinkedIn",
  "Podcast",
  "Blog/Newsletter",
];

export default function CreatorProfilePage() {
  const [form, setForm] = useState({
    niche: "Personal finance",
    platforms: ["TikTok", "Instagram Reels", "YouTube Shorts"],
    followers: 25000,
    audience: "USA young professionals, age 22-35",
    region: "United States",
    skills:
      "Budgeting tips, money-saving education, short-form video storytelling",
    business_interest: "Digital products + affiliate marketing",
    income_goal: "$2,000/month in 6 months",
    available_time: "2 hours/day",
    current_challenge:
      "I create helpful content but need a clear roadmap to turn my audience into a digital business.",
  });

  const [result, setResult] = useState<ProfileResult | null>(null);
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

  async function handleSubmit() {
    try {
      setLoading(true);
      setError("");
      setResult(null);

      const response = await api.post("/profile/analyze", form);
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
            <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-fuchsia-500/30 bg-fuchsia-500/10 px-4 py-2 text-sm font-bold text-fuchsia-200">
              <User size={16} />
              Creator Profile Setup
            </div>

            <h1 className="text-4xl font-black tracking-tight md:text-5xl">
              Build your creator business foundation.
            </h1>

            <p className="mt-3 max-w-3xl text-slate-400">
              Add your niche, audience, platforms, skills, and income goal.
              CreatorCareer AI will analyze your creator stage and suggest the
              best business direction.
            </p>
          </div>

          <a
            href="/dashboard"
            className="rounded-xl border border-white/10 bg-white/5 px-5 py-3 text-sm font-bold text-slate-200 hover:bg-white/10"
          >
            Back to Dashboard
          </a>
        </header>

        <div className="grid gap-6 lg:grid-cols-[1fr_0.85fr]">
          <section className="rounded-3xl border border-white/10 bg-[#0c1428] p-6 shadow-[0_0_50px_rgba(168,85,247,0.12)]">
            <div className="mb-6 flex items-center gap-3">
              <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-to-br from-violet-600 to-fuchsia-500">
                <Sparkles size={22} />
              </div>

              <div>
                <h2 className="text-xl font-black">Creator Information</h2>
                <p className="text-sm text-slate-400">
                  This data will personalize all AI modules.
                </p>
              </div>
            </div>

            <div className="grid gap-5">
              <Input
                label="Creator Niche"
                value={form.niche}
                onChange={(value) => updateField("niche", value)}
                placeholder="Example: Personal finance, fitness, beauty"
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

              <Textarea
                label="Creator Skills"
                value={form.skills}
                onChange={(value) => updateField("skills", value)}
                placeholder="Budgeting tips, storytelling, video creation"
              />

              <Input
                label="Business Interest"
                value={form.business_interest}
                onChange={(value) =>
                  updateField("business_interest", value)
                }
                placeholder="Digital products + affiliate marketing"
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
                label="Current Challenge"
                value={form.current_challenge}
                onChange={(value) =>
                  updateField("current_challenge", value)
                }
                placeholder="What is the biggest problem in your creator journey?"
              />

              {error && (
                <div className="rounded-2xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-200">
                  {error}
                </div>
              )}

              <button
                onClick={handleSubmit}
                disabled={loading}
                className="mt-2 flex items-center justify-center gap-3 rounded-2xl bg-gradient-to-r from-rose-500 via-fuchsia-500 to-orange-500 px-6 py-4 font-black text-white shadow-[0_0_30px_rgba(217,70,239,0.35)] disabled:cursor-not-allowed disabled:opacity-60"
              >
                {loading ? (
                  <>
                    <Loader2 className="animate-spin" size={20} />
                    Analyzing Creator Profile...
                  </>
                ) : (
                  <>
                    Analyze Creator Profile
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
                  Your AI profile report will appear here.
                </h2>

                <p className="mt-3 text-slate-400">
                  Fill the form and run the analysis to generate creator
                  positioning, opportunity, readiness score, and next action.
                </p>
              </div>
            ) : (
              <>
                <div className="rounded-3xl border border-fuchsia-500/30 bg-gradient-to-br from-violet-950/70 to-slate-950 p-6 shadow-[0_0_50px_rgba(217,70,239,0.18)]">
                  <div className="flex items-center justify-between gap-4">
                    <div>
                      <p className="text-sm font-bold uppercase tracking-[0.2em] text-fuchsia-300">
                        Business Readiness
                      </p>

                      <h2 className="mt-2 text-5xl font-black">
                        {result.business_readiness_score}
                        <span className="text-xl text-slate-400">/100</span>
                      </h2>

                      <p className="mt-2 text-slate-300">
                        {result.creator_stage}
                      </p>
                    </div>

                    <div className="flex h-24 w-24 items-center justify-center rounded-full bg-gradient-to-br from-fuchsia-500 to-orange-500">
                      <Rocket size={42} />
                    </div>
                  </div>
                </div>

                <ResultCard
                  icon={User}
                  title="Creator Summary"
                  text={result.creator_summary}
                />

                <ResultCard
                  icon={Target}
                  title="Niche Positioning"
                  text={result.niche_positioning}
                />

                <ResultCard
                  icon={Users}
                  title="Audience Opportunity"
                  text={result.audience_opportunity}
                />

                <ResultCard
                  icon={BriefcaseBusiness}
                  title="Business Opportunity"
                  text={result.business_opportunity}
                />

                <div className="rounded-3xl border border-white/10 bg-[#0c1428] p-6">
                  <h3 className="mb-4 flex items-center gap-2 text-xl font-black">
                    <CheckCircle2 className="text-emerald-400" />
                    Recommended Next Modules
                  </h3>

                  <div className="grid gap-3">
                    {result.recommended_next_modules.map((module) => (
                      <div
                        key={module}
                        className="rounded-xl border border-white/10 bg-white/5 p-4 text-sm font-semibold text-slate-200"
                      >
                        {module}
                      </div>
                    ))}
                  </div>
                </div>

                <div className="rounded-3xl border border-orange-500/30 bg-orange-500/10 p-6">
                  <h3 className="mb-3 flex items-center gap-2 text-xl font-black">
                    <Clock className="text-orange-300" />
                    Next Best Action
                  </h3>

                  <p className="leading-7 text-slate-200">
                    {result.next_best_action}
                  </p>
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
        rows={4}
        className="w-full resize-none rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-white outline-none placeholder:text-slate-500 focus:border-fuchsia-500/60"
      />
    </div>
  );
}

function ResultCard({
  icon: Icon,
  title,
  text,
}: {
  icon: ElementType;
  title: string;
  text: string;
}) {
  return (
    <div className="rounded-3xl border border-white/10 bg-[#0c1428] p-6">
      <h3 className="mb-3 flex items-center gap-2 text-xl font-black">
        <Icon className="text-fuchsia-300" />
        {title}
      </h3>

      <p className="leading-7 text-slate-300">{text}</p>
    </div>
  );
}


