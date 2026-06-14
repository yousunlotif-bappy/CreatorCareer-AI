"use client";

import { useState, type ElementType } from "react";
import {
  ArrowRight,
  Bot,
  Captions,
  Clapperboard,
  Copy,
  FileText,
  Film,
  Hash,
  Loader2,
  MessageSquareText,
  PlaySquare,
  Sparkles,
  Target,
  WandSparkles,
} from "lucide-react";

import AiProofCard from "@/components/AiProofCard";
import { api } from "@/lib/api";

type ContentResult = {
  titles: string[];
  hook: string;
  voiceover_script: string;
  caption: string;
  hashtags: string[];
  thumbnail_text: string[];
  cta: string;
  platform_notes: string;
  scene_breakdown: string[];
  video_generation_prompt: string;
  b_roll_ideas: string[];
  editing_notes: string[];
  status: string;
};

export default function ContentPackagePage() {
  const [form, setForm] = useState({
    topic: "5 budgeting mistakes young professionals make",
    platform: "TikTok + Instagram Reels",
    audience: "USA young professionals, age 22-35",
    tone: "Helpful and engaging",
    duration: "30 seconds",
    language: "English",
    content_goal: "Build awareness and save-worthy educational content",

    // New Day 4 upgrade fields
    story_or_video_reference:
      "A young professional checks monthly spending, realizes small daily expenses are hurting savings, then learns a simple budgeting habit.",
    video_style: "modern cinematic, clean captions, fast social media pacing",
  });

  const [result, setResult] = useState<ContentResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function updateField(field: keyof typeof form, value: string) {
    setForm((previousForm) => ({
      ...previousForm,
      [field]: value,
    }));
  }

  async function handleGenerate() {
    try {
      setLoading(true);
      setError("");
      setResult(null);

      const response = await api.post("/content/package", form);
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
              <WandSparkles size={16} />
              AI Content Package Generator
            </div>

            <h1 className="text-4xl font-black tracking-tight md:text-5xl">
              Turn one topic into a full content package.
            </h1>

            <p className="mt-3 max-w-3xl text-slate-400">
              Import a story or video idea, then generate titles, hook,
              voiceover script, caption, hashtags, thumbnail text, CTA, and an
              AI video generation plan.
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
              <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-to-br from-fuchsia-600 to-orange-500">
                <Sparkles size={22} />
              </div>

              <div>
                <h2 className="text-xl font-black">Content + Video Input</h2>
                <p className="text-sm text-slate-400">
                  Give AI the topic, story/video idea, audience, tone, and
                  platform.
                </p>
              </div>
            </div>

            <div className="grid gap-5">
              <Textarea
                label="Content Topic"
                value={form.topic}
                onChange={(value) => updateField("topic", value)}
                placeholder="Example: 5 budgeting mistakes young professionals make"
              />

              <Textarea
                label="Import Story / Video Idea"
                value={form.story_or_video_reference}
                onChange={(value) =>
                  updateField("story_or_video_reference", value)
                }
                placeholder="Paste your story, video idea, rough script, scene idea, or reference concept here..."
              />

              <Input
                label="AI Video Style"
                value={form.video_style}
                onChange={(value) => updateField("video_style", value)}
                placeholder="Modern cinematic, realistic, animated, documentary, clean captions..."
              />

              <Input
                label="Platform"
                value={form.platform}
                onChange={(value) => updateField("platform", value)}
                placeholder="TikTok + Instagram Reels"
              />

              <Input
                label="Target Audience"
                value={form.audience}
                onChange={(value) => updateField("audience", value)}
                placeholder="USA young professionals, age 22-35"
              />

              <Input
                label="Tone"
                value={form.tone}
                onChange={(value) => updateField("tone", value)}
                placeholder="Helpful and engaging"
              />

              <Input
                label="Duration"
                value={form.duration}
                onChange={(value) => updateField("duration", value)}
                placeholder="30 seconds"
              />

              <Input
                label="Language"
                value={form.language}
                onChange={(value) => updateField("language", value)}
                placeholder="English"
              />

              <Textarea
                label="Content Goal"
                value={form.content_goal}
                onChange={(value) => updateField("content_goal", value)}
                placeholder="Build awareness, educate, sell, grow engagement..."
              />

              {error && (
                <div className="rounded-2xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-200">
                  {error}
                </div>
              )}

              <button
                onClick={handleGenerate}
                disabled={loading}
                className="mt-2 flex items-center justify-center gap-3 rounded-2xl bg-gradient-to-r from-rose-500 via-fuchsia-500 to-orange-500 px-6 py-4 font-black text-white shadow-[0_0_30px_rgba(217,70,239,0.35)] disabled:cursor-not-allowed disabled:opacity-60"
              >
                {loading ? (
                  <>
                    <Loader2 className="animate-spin" size={20} />
                    Generating Package + Video Plan...
                  </>
                ) : (
                  <>
                    Generate Package + Video Plan
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
                  Your AI content and video package will appear here.
                </h2>

                <p className="mt-3 text-slate-400">
                  Import a topic or story idea, then generate platform-ready
                  content and an AI video generation plan.
                </p>
              </div>
            ) : (
              <>
                <AiProofCard
                  result={result as unknown as Record<string, unknown>}
                />

                <ResultSection
                  icon={PlaySquare}
                  title="Title Ideas"
                  items={result.titles}
                  onCopy={copyText}
                />

                <SingleResult
                  icon={Target}
                  title="Opening Hook"
                  text={result.hook}
                  onCopy={copyText}
                />

                <SingleResult
                  icon={MessageSquareText}
                  title="Voiceover Script"
                  text={result.voiceover_script}
                  onCopy={copyText}
                />

                <SingleResult
                  icon={Captions}
                  title="Caption"
                  text={result.caption}
                  onCopy={copyText}
                />

                <ResultSection
                  icon={Hash}
                  title="Hashtags"
                  items={result.hashtags}
                  onCopy={copyText}
                />

                <ResultSection
                  icon={FileText}
                  title="Thumbnail Text"
                  items={result.thumbnail_text}
                  onCopy={copyText}
                />

                <SingleResult
                  icon={ArrowRight}
                  title="Call To Action"
                  text={result.cta}
                  onCopy={copyText}
                />

                <SingleResult
                  icon={Sparkles}
                  title="Platform Notes"
                  text={result.platform_notes}
                  onCopy={copyText}
                />

                <ResultSection
                  icon={Clapperboard}
                  title="AI Scene Breakdown"
                  items={result.scene_breakdown}
                  onCopy={copyText}
                />

                <SingleResult
                  icon={Film}
                  title="AI Video Generation Prompt"
                  text={result.video_generation_prompt}
                  onCopy={copyText}
                />

                <ResultSection
                  icon={PlaySquare}
                  title="B-roll / Visual Ideas"
                  items={result.b_roll_ideas}
                  onCopy={copyText}
                />

                <ResultSection
                  icon={WandSparkles}
                  title="Video Editing Notes"
                  items={result.editing_notes}
                  onCopy={copyText}
                />

                <div className="rounded-3xl border border-emerald-500/30 bg-emerald-500/10 p-5 text-sm text-emerald-200">
                  {result.status}
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




