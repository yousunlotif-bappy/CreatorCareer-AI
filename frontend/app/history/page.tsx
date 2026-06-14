"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import {
  ArrowLeft,
  Bot,
  ClipboardList,
  Database,
  FileText,
  Gauge,
  History,
  Layers,
  LineChart,
  Loader2,
  PackageCheck,
  RefreshCcw,
  ShieldCheck,
  Sparkles,
  User,
} from "lucide-react";

import { api } from "@/lib/api";

type HistoryGroup = {
  key: string;
  title: string;
  description: string;
  endpoint: string;
  icon: typeof User;
  items: unknown[];
  loading: boolean;
  error: string;
};

function getPreviewText(item: unknown) {
  if (!item || typeof item !== "object") {
    return "Saved output";
  }

  const record = item as Record<string, unknown>;

  const possibleFields = [
    "name",
    "title",
    "topic",
    "niche",
    "product_idea",
    "summary",
    "status",
    "created_at",
  ];

  for (const field of possibleFields) {
    const value = record[field];

    if (typeof value === "string" && value.trim().length > 0) {
      return value;
    }

    if (typeof value === "number") {
      return String(value);
    }
  }

  return "Saved database record";
}

function getDateText(item: unknown) {
  if (!item || typeof item !== "object") {
    return "Recently saved";
  }

  const record = item as Record<string, unknown>;

  const dateValue =
    record.created_at ||
    record.inserted_at ||
    record.updated_at ||
    record.date ||
    record.timestamp;

  if (typeof dateValue !== "string") {
    return "Recently saved";
  }

  const date = new Date(dateValue);

  if (Number.isNaN(date.getTime())) {
    return dateValue;
  }

  return date.toLocaleString();
}

function safeCount(items: unknown[]) {
  return Array.isArray(items) ? items.length : 0;
}

export default function HistoryPage() {
  const [groups, setGroups] = useState<HistoryGroup[]>([
    {
      key: "creators",
      title: "Creator Profiles",
      description: "Saved creator profile information from Supabase.",
      endpoint: "/db/latest-creators",
      icon: User,
      items: [],
      loading: true,
      error: "",
    },
    {
      key: "content",
      title: "Content Packages",
      description: "AI-generated titles, hooks, scripts, captions, and video plans.",
      endpoint: "/db/latest-content",
      icon: PackageCheck,
      items: [],
      loading: true,
      error: "",
    },
    {
      key: "market",
      title: "Market Analysis",
      description: "Saved niche, audience, product, and market opportunity analysis.",
      endpoint: "/db/latest-market-analysis",
      icon: LineChart,
      items: [],
      loading: true,
      error: "",
    },
    {
      key: "product",
      title: "Product Validation",
      description: "Product scores, risks, recommendations, and checklist outputs.",
      endpoint: "/db/latest-product-scores",
      icon: Gauge,
      items: [],
      loading: true,
      error: "",
    },
    {
      key: "affiliate",
      title: "Affiliate Roadmaps",
      description: "Saved affiliate and dropshipping roadmap results.",
      endpoint: "/db/latest-affiliate-roadmaps",
      icon: ClipboardList,
      items: [],
      loading: true,
      error: "",
    },
    {
      key: "ethical",
      title: "Ethical Checks",
      description: "Saved ethical monetization checks and safer promotion suggestions.",
      endpoint: "/db/latest-ethical-checks",
      icon: ShieldCheck,
      items: [],
      loading: true,
      error: "",
    },
    {
      key: "agents",
      title: "7-Agent Reports",
      description: "Saved creator business readiness and roadmap reports.",
      endpoint: "/db/latest-seven-agent-reports",
      icon: Bot,
      items: [],
      loading: true,
      error: "",
    },
    {
      key: "reports",
      title: "PDF Reports",
      description: "Saved downloadable business report history.",
      endpoint: "/db/latest-reports",
      icon: FileText,
      items: [],
      loading: true,
      error: "",
    },
  ]);

  async function loadHistory() {
    setGroups((previousGroups) =>
      previousGroups.map((group) => ({
        ...group,
        loading: true,
        error: "",
      })),
    );

    const updatedGroups = await Promise.all(
      groups.map(async (group) => {
        try {
          const response = await api.get(group.endpoint);

          const data = response.data;

          let items: unknown[] = [];

          if (Array.isArray(data)) {
            items = data;
          } else if (data && typeof data === "object") {
            const record = data as Record<string, unknown>;

            const possibleArray =
              record.data ||
              record.items ||
              record.results ||
              record.creators ||
              record.content ||
              record.market_analysis ||
              record.product_scores ||
              record.affiliate_roadmaps ||
              record.ethical_checks ||
              record.seven_agent_reports ||
              record.reports;

            if (Array.isArray(possibleArray)) {
              items = possibleArray;
            } else {
              items = [data];
            }
          }

          return {
            ...group,
            items,
            loading: false,
            error: "",
          };
        } catch {
          return {
            ...group,
            items: [],
            loading: false,
            error: "Could not load this history section.",
          };
        }
      }),
    );

    setGroups(updatedGroups);
  }

  useEffect(() => {
    loadHistory();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const totalRecords = groups.reduce(
    (total, group) => total + safeCount(group.items),
    0,
  );

  const loadingCount = groups.filter((group) => group.loading).length;

  return (
    <main className="min-h-screen bg-[#030816] px-5 py-8 text-white md:px-10">
      <div className="mx-auto max-w-7xl">
        <header className="mb-8 flex flex-col gap-5 md:flex-row md:items-end md:justify-between">
          <div>
            <Link
              href="/dashboard"
              className="mb-4 inline-flex items-center gap-2 rounded-xl border border-white/10 bg-white/5 px-4 py-2 text-sm font-bold text-slate-300 transition hover:bg-white/10 hover:text-white"
            >
              <ArrowLeft size={17} />
              Back to Dashboard
            </Link>

            <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-fuchsia-500/30 bg-fuchsia-500/10 px-4 py-2 text-sm font-bold text-fuchsia-200">
              <History size={16} />
              Saved History
            </div>

            <h1 className="text-4xl font-black tracking-tight md:text-5xl">
              Database-backed creator history.
            </h1>

            <p className="mt-3 max-w-3xl text-slate-400">
              View saved creator profiles, AI content outputs, market analysis,
              product validation, affiliate roadmap, ethical checks, 7-agent
              reports, and generated report history.
            </p>
          </div>

          <button
            onClick={loadHistory}
            className="inline-flex items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-fuchsia-500 to-orange-500 px-5 py-3 text-sm font-black text-white transition hover:opacity-90"
          >
            <RefreshCcw size={17} />
            Refresh History
          </button>
        </header>

        <section className="mb-6 grid gap-4 md:grid-cols-3">
          <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-5">
            <div className="flex items-center gap-3">
              <div className="rounded-xl bg-fuchsia-500/15 p-3 text-fuchsia-300">
                <Database size={24} />
              </div>

              <div>
                <p className="text-sm text-slate-400">Total Records</p>
                <p className="text-3xl font-black">{totalRecords}</p>
              </div>
            </div>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-5">
            <div className="flex items-center gap-3">
              <div className="rounded-xl bg-orange-500/15 p-3 text-orange-300">
                <Layers size={24} />
              </div>

              <div>
                <p className="text-sm text-slate-400">History Sections</p>
                <p className="text-3xl font-black">{groups.length}</p>
              </div>
            </div>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-5">
            <div className="flex items-center gap-3">
              <div className="rounded-xl bg-emerald-500/15 p-3 text-emerald-300">
                <Sparkles size={24} />
              </div>

              <div>
                <p className="text-sm text-slate-400">System Status</p>
                <p className="text-3xl font-black">
                  {loadingCount > 0 ? "Loading" : "Ready"}
                </p>
              </div>
            </div>
          </div>
        </section>

        <section className="grid gap-5 lg:grid-cols-2">
          {groups.map((group) => {
            const Icon = group.icon;

            return (
              <div
                key={group.key}
                className="rounded-3xl border border-white/10 bg-[#0c1428] p-6 shadow-[0_0_35px_rgba(15,23,42,0.22)]"
              >
                <div className="mb-5 flex items-start justify-between gap-4">
                  <div className="flex items-start gap-4">
                    <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-br from-fuchsia-600/30 to-orange-500/30 text-fuchsia-200 ring-1 ring-white/10">
                      <Icon size={23} />
                    </div>

                    <div>
                      <h2 className="text-xl font-black">{group.title}</h2>
                      <p className="mt-1 text-sm leading-6 text-slate-400">
                        {group.description}
                      </p>
                    </div>
                  </div>

                  <span className="rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm font-black text-slate-200">
                    {safeCount(group.items)}
                  </span>
                </div>

                {group.loading ? (
                  <div className="flex items-center gap-3 rounded-2xl border border-white/10 bg-white/5 p-4 text-slate-300">
                    <Loader2 className="animate-spin" size={18} />
                    Loading saved records...
                  </div>
                ) : group.error ? (
                  <div className="rounded-2xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-200">
                    {group.error}
                  </div>
                ) : group.items.length === 0 ? (
                  <div className="rounded-2xl border border-white/10 bg-white/5 p-4 text-sm text-slate-400">
                    No saved records found yet. Generate and save output from
                    this module first.
                  </div>
                ) : (
                  <div className="space-y-3">
                    {group.items.slice(0, 4).map((item, index) => (
                      <div
                        key={`${group.key}-${index}`}
                        className="rounded-2xl border border-white/10 bg-white/[0.04] p-4"
                      >
                        <p className="line-clamp-2 font-bold text-slate-100">
                          {getPreviewText(item)}
                        </p>

                        <p className="mt-2 text-xs text-slate-500">
                          {getDateText(item)}
                        </p>
                      </div>
                    ))}

                    {group.items.length > 4 && (
                      <p className="text-right text-sm text-fuchsia-300">
                        +{group.items.length - 4} more saved records
                      </p>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </section>
      </div>
    </main>
  );
}


