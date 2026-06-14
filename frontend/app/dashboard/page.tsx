import Image from "next/image";
import Link from "next/link";

import {
  Bell,
  Bot,
  BriefcaseBusiness,
  CalendarDays,
  ChevronDown,
  ClipboardList,
  Download,
  FileText,
  Gauge,
  Home,
  LineChart,
  PackageCheck,
  Rocket,
  Search,
  Settings,
  ShieldCheck,
  ShoppingCart,
  Sparkles,
  Target,
  TrendingUp,
  User,
  Zap,
} from "lucide-react";

import LiveSystemStatus from "@/components/LiveSystemStatus";
import {
  actionPlan,
  agentCards,
  recommendedProducts,
  scoreCards,
} from "@/lib/dashboard-data";

/*
  Dashboard Page
  --------------
  This file is fully replacement-ready.

  Main improvements:
  - More professional compact sidebar
  - Better logo spacing and branding
  - Cleaner sidebar navigation
  - Creator Pro Plan moved to the right side of topbar
  - Better topbar alignment
  - Live system status added after topbar
*/

const LOGO_SRC = "/logo1.png";

/*
  Sidebar Navigation
  ------------------
  Dashboard is active here because this is the dashboard page.
*/
const navItems = [
  {
    label: "Dashboard",
    icon: Home,
    href: "/dashboard",
    active: true,
  },
  {
    label: "Creator Profile",
    icon: User,
    href: "/profile",
  },
  {
    label: "Content Package",
    icon: PackageCheck,
    href: "/content-package",
  },
  {
    label: "Market Analysis",
    icon: LineChart,
    href: "/market-analysis",
  },
  {
    label: "Product Validation",
    icon: Gauge,
    href: "/product-validation",
  },
  {
    label: "Affiliate Roadmap",
    icon: ClipboardList,
    href: "/affiliate-roadmap",
  },
  {
    label: "Ethical Checker",
    icon: ShieldCheck,
    href: "/ethical-checker",
  },
  {
    label: "7-Agent Dashboard",
    icon: Bot,
    href: "/seven-agent-dashboard",
  },
  {
    label: "Saved History",
    icon: FileText,
    href: "/history",
  },
  {
    label: "Reports",
    icon: Download,
    href: "/reports",
  },
  {
    label: "Settings",
    icon: Settings,
    href: "/settings",
  },
];

const heroFeatures = [
  {
    title: "Create.",
    subtitle: "Build with clarity",
    icon: Zap,
  },
  {
    title: "Grow.",
    subtitle: "Scale with strategy",
    icon: TrendingUp,
  },
  {
    title: "Monetize.",
    subtitle: "Profit with purpose",
    icon: BriefcaseBusiness,
  },
];

const dashboardShortcuts = [
  {
    title: "Market Analysis",
    description: "Find product opportunities from niche and audience signals.",
    icon: LineChart,
    href: "/market-analysis",
    accent: "orange",
  },
  {
    title: "Ethical Monetization",
    description: "Check disclosure, claims, transparency, and trust signals.",
    icon: ShieldCheck,
    href: "/ethical-checker",
    accent: "amber",
  },
  {
    title: "7-Agent Dashboard",
    description: "Run a full creator business analysis using seven agents.",
    icon: Bot,
    href: "/seven-agent-dashboard",
    accent: "purple",
  },
];

/*
  Logo
  ----
  Professional compact branding for the sidebar.
*/
function Logo() {
  return (
    <Link href="/dashboard" className="block">
      <div className="flex items-center gap-3 rounded-2xl border border-white/10 bg-white/[0.03] p-3">
        <div className="relative h-14 w-14 shrink-0 overflow-hidden rounded-2xl border border-fuchsia-500/30 bg-slate-950 shadow-[0_0_24px_rgba(217,70,239,0.25)]">
          <Image
            src={LOGO_SRC}
            alt="CreatorCareer AI Logo"
            fill
            priority
            sizes="56px"
            className="object-contain p-1"
          />
        </div>

        <div className="min-w-0">
          <h1 className="text-lg font-black leading-tight tracking-tight text-white">
            CreatorCareer
          </h1>

          <p className="bg-gradient-to-r from-fuchsia-400 to-orange-400 bg-clip-text text-sm font-black text-transparent">
            AI Platform
          </p>
        </div>
      </div>
    </Link>
  );
}

/*
  Sidebar
  -------
  More professional sidebar:
  - Compact logo
  - Clean navigation
  - Less empty space
  - Better active state
*/
function Sidebar() {
  return (
    <aside className="sticky top-0 hidden h-screen w-[280px] shrink-0 overflow-y-auto border-r border-white/10 bg-[#06101f]/95 px-4 py-5 backdrop-blur-xl lg:block">
      <Logo />

      <div className="mt-6">
        <p className="mb-3 px-3 text-[11px] font-bold uppercase tracking-[0.22em] text-slate-500">
          Workspace
        </p>

        <nav className="space-y-1.5">
          {navItems.map((item) => {
            const Icon = item.icon;

            return (
              <Link
                key={item.label}
                href={item.href}
                className={`group flex items-center gap-3 rounded-xl px-3.5 py-3 text-sm font-semibold transition ${
                  item.active
                    ? "bg-gradient-to-r from-fuchsia-500/20 to-orange-500/10 text-white ring-1 ring-fuchsia-500/30 shadow-[0_0_24px_rgba(217,70,239,0.14)]"
                    : "text-slate-400 hover:bg-white/[0.06] hover:text-white"
                }`}
              >
                <span
                  className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-lg transition ${
                    item.active
                      ? "bg-fuchsia-500/20 text-fuchsia-200"
                      : "bg-white/[0.04] text-slate-400 group-hover:text-white"
                  }`}
                >
                  <Icon size={18} />
                </span>

                <span className="truncate">{item.label}</span>
              </Link>
            );
          })}
        </nav>
      </div>

      <div className="mt-6 rounded-2xl border border-orange-500/25 bg-gradient-to-br from-violet-950/50 via-slate-950 to-orange-950/30 p-4">
        <div className="flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-fuchsia-500/15 text-fuchsia-300">
            <Rocket size={22} />
          </div>

          <div>
            <h3 className="text-sm font-black text-white">Demo Ready</h3>
            <p className="text-xs text-slate-400">Creator business OS</p>
          </div>
        </div>

        <p className="mt-4 text-sm leading-6 text-slate-300">
          Run the full workflow from profile to PDF report and saved history.
        </p>

        <Link
          href="/seven-agent-dashboard"
          className="mt-4 block rounded-xl bg-gradient-to-r from-fuchsia-500 to-orange-500 px-4 py-3 text-center text-sm font-black text-white transition hover:opacity-90"
        >
          Run 7-Agent Demo
        </Link>
      </div>
    </aside>
  );
}

/*
  Topbar
  ------
  Creator Pro Plan is forced to the right side.
*/
function Topbar() {
  return (
    <header className="rounded-2xl border border-white/10 bg-white/[0.04] p-4 shadow-[0_0_35px_rgba(15,23,42,0.25)] backdrop-blur-xl">
      <div className="flex flex-col gap-4 xl:flex-row xl:items-center">
        <div className="shrink-0">
          <h2 className="text-2xl font-black leading-tight text-white">
            Welcome back, Creator! 👋
          </h2>
          <p className="mt-1 text-sm text-slate-400">
            Here&apos;s your creator business overview.
          </p>
        </div>

        <div className="flex flex-1 flex-wrap items-center gap-3 xl:justify-end">
          <div className="hidden min-w-[320px] max-w-[460px] flex-1 items-center gap-3 rounded-xl border border-white/10 bg-slate-950/70 px-4 py-3 text-slate-400 lg:flex">
            <Search size={18} />
            <span className="truncate text-sm">
              Search insights, content, tools...
            </span>
            <span className="ml-auto rounded-md border border-white/10 px-2 py-0.5 text-xs">
              ⌘K
            </span>
          </div>

          <Link
            href="/seven-agent-dashboard"
            className="flex items-center gap-2 rounded-xl border border-orange-500/20 bg-gradient-to-r from-orange-500/15 to-fuchsia-600/15 px-5 py-3 text-sm font-bold text-white transition hover:border-fuchsia-500/40 hover:bg-fuchsia-500/10"
          >
            <Sparkles size={18} className="text-orange-400" />
            AI Assistant
          </Link>

          <button className="relative rounded-xl border border-white/10 bg-slate-950/70 p-3 text-white transition hover:bg-white/10">
            <Bell size={20} />
            <span className="absolute -right-1 -top-1 flex h-5 w-5 items-center justify-center rounded-full bg-fuchsia-600 text-xs font-bold">
              3
            </span>
          </button>

          <div className="ml-0 flex items-center gap-3 rounded-xl border border-white/10 bg-slate-950/70 px-3 py-2 xl:ml-2">
            <div className="flex h-11 w-11 items-center justify-center rounded-full border border-orange-400/50 bg-gradient-to-br from-orange-400 to-fuchsia-600 font-black text-white">
              C
            </div>

            <div className="hidden text-left sm:block">
              <p className="text-sm font-black text-white">Creator</p>
              <p className="text-xs font-medium text-slate-400">Pro Plan</p>
            </div>

            <ChevronDown size={18} className="text-slate-400" />
          </div>
        </div>
      </div>
    </header>
  );
}

function HeroBanner() {
  return (
    <section className="relative overflow-hidden rounded-2xl border border-white/10 bg-[#0c1230] p-6 shadow-[0_0_45px_rgba(147,51,234,0.18)]">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_75%_40%,rgba(147,51,234,0.55),transparent_32%),radial-gradient(circle_at_90%_80%,rgba(249,115,22,0.28),transparent_30%)]" />

      <div className="absolute -right-10 top-0 hidden h-full w-[430px] opacity-90 lg:block">
        <div className="absolute right-28 top-12 flex h-36 w-36 items-center justify-center rounded-full border-[18px] border-white bg-slate-950">
          <div className="ml-2 h-0 w-0 border-y-[20px] border-l-[32px] border-y-transparent border-l-orange-400" />
        </div>

        <TrendingUp
          className="absolute bottom-8 right-16 text-orange-400"
          size={115}
        />

        <Sparkles
          className="absolute right-40 top-8 text-orange-400"
          size={34}
        />

        <div className="absolute bottom-5 right-44 flex items-end gap-2">
          <div className="h-8 w-4 rounded bg-white" />
          <div className="h-14 w-4 rounded bg-white" />
          <div className="h-20 w-4 rounded bg-white" />
        </div>
      </div>

      <div className="relative max-w-2xl">
        <p className="mb-4 w-fit rounded-full border border-fuchsia-500/40 bg-fuchsia-500/10 px-4 py-2 text-xs font-bold uppercase tracking-[0.22em] text-fuchsia-300">
          7-Agent Creator Business OS
        </p>

        <h1 className="text-4xl font-black md:text-6xl">
          CreatorCareer AI
        </h1>

        <p className="mt-3 text-xl text-slate-200">
          Turn content into business.
        </p>

        <div className="mt-6 grid gap-3 md:grid-cols-3">
          {heroFeatures.map((item) => {
            const Icon = item.icon;

            return (
              <div
                key={item.title}
                className="rounded-xl border border-white/10 bg-white/[0.05] p-4 backdrop-blur"
              >
                <div className="flex items-center gap-3">
                  <Icon className="text-fuchsia-400" size={22} />

                  <div>
                    <p className="font-bold">{item.title}</p>
                    <p className="text-xs text-slate-400">{item.subtitle}</p>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        <div className="mt-6 flex flex-wrap gap-4">
          <Link
            href="/market-analysis"
            className="rounded-xl bg-gradient-to-r from-fuchsia-500 to-orange-500 px-7 py-3 text-sm font-black text-white transition hover:opacity-90"
          >
            Explore Insights →
          </Link>

          <Link
            href="/seven-agent-dashboard"
            className="rounded-xl border border-white/15 bg-slate-950/60 px-7 py-3 text-sm font-bold text-white transition hover:bg-white/5"
          >
            View 7-Agent Dashboard
          </Link>
        </div>
      </div>
    </section>
  );
}

function DashboardShortcuts() {
  return (
    <section className="grid gap-4 md:grid-cols-3">
      {dashboardShortcuts.map((item) => {
        const Icon = item.icon;

        const accentClass =
          item.accent === "purple"
            ? "text-violet-400"
            : item.accent === "orange"
              ? "text-orange-400"
              : "text-amber-400";

        return (
          <Link
            key={item.title}
            href={item.href}
            className="group rounded-2xl border border-white/10 bg-white/[0.04] p-5 transition hover:-translate-y-1 hover:border-fuchsia-500/40 hover:bg-white/[0.06]"
          >
            <div className="flex items-start gap-4">
              <div className="rounded-xl border border-white/10 bg-slate-950/60 p-3">
                <Icon className={accentClass} size={24} />
              </div>

              <div>
                <h3 className="font-bold text-white">{item.title}</h3>
                <p className="mt-2 text-sm leading-6 text-slate-400">
                  {item.description}
                </p>
              </div>
            </div>

            <p className="mt-4 text-right text-fuchsia-400">Open →</p>
          </Link>
        );
      })}
    </section>
  );
}

function ScoreCards() {
  return (
    <section className="grid gap-4 md:grid-cols-2 2xl:grid-cols-4">
      {scoreCards.map((card) => {
        const scoreColor =
          card.color === "purple"
            ? "text-violet-400"
            : card.color === "pink"
              ? "text-pink-500"
              : card.color === "orange"
                ? "text-orange-500"
                : "text-amber-400";

        const barColor =
          card.color === "purple"
            ? "bg-violet-500"
            : card.color === "pink"
              ? "bg-pink-500"
              : card.color === "orange"
                ? "bg-orange-500"
                : "bg-amber-400";

        return (
          <div
            key={card.title}
            className="rounded-2xl border border-white/10 bg-white/[0.04] p-5 backdrop-blur"
          >
            <div className="flex items-center justify-between">
              <p className="text-sm font-bold text-white">{card.title}</p>
              <span className="text-xs text-emerald-400">↑ {card.growth}</span>
            </div>

            <div className="mt-4 flex items-end gap-1">
              <span className={`text-4xl font-black ${scoreColor}`}>
                {card.value}
              </span>

              <span className="pb-1 text-xl text-slate-400">
                {card.suffix}
              </span>
            </div>

            <div className="mt-4 flex h-7 items-end gap-2">
              {[22, 30, 18, 27, 36, 20, 39, 35, 47].map((height, index) => (
                <div
                  key={index}
                  style={{ height }}
                  className={`w-full rounded-full ${barColor}`}
                />
              ))}
            </div>

            <p className="mt-4 text-sm text-slate-400">● {card.status}</p>
          </div>
        );
      })}
    </section>
  );
}

function AgentDashboard() {
  const iconList = [
    Bot,
    Target,
    User,
    ShoppingCart,
    BriefcaseBusiness,
    ShieldCheck,
    CalendarDays,
  ];

  return (
    <section className="rounded-2xl border border-white/10 bg-white/[0.04] p-5 backdrop-blur">
      <h3 className="text-xl font-black text-white">
        7-Agent Creator Business Dashboard
      </h3>

      <p className="mt-2 text-sm text-slate-400">
        A focused AI workflow for creator product strategy, affiliate planning,
        ethical monetization, validation, and launch roadmap.
      </p>

      <div className="mt-4 grid gap-4 md:grid-cols-2 2xl:grid-cols-3">
        {agentCards.map((agent, index) => {
          const Icon = iconList[index] || Bot;

          const accentClass =
            agent.accent === "purple"
              ? "border-violet-500/50 bg-violet-500/10 text-violet-400"
              : agent.accent === "pink"
                ? "border-pink-500/50 bg-pink-500/10 text-pink-400"
                : agent.accent === "orange"
                  ? "border-orange-500/50 bg-orange-500/10 text-orange-400"
                  : "border-amber-400/50 bg-amber-400/10 text-amber-400";

          return (
            <Link
              key={agent.title}
              href="/seven-agent-dashboard"
              className="group rounded-xl border border-white/10 bg-slate-950/40 p-4 transition hover:border-fuchsia-500/40 hover:bg-slate-900"
            >
              <div className="flex items-start gap-4">
                <div
                  className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-full border ${accentClass}`}
                >
                  <Icon size={24} />
                </div>

                <div>
                  <h4 className="font-bold leading-5 text-white">
                    {agent.title}
                  </h4>
                  <p className="mt-2 text-sm leading-5 text-slate-400">
                    {agent.description}
                  </p>
                </div>
              </div>

              <p className="mt-3 text-right text-lg text-fuchsia-400">→</p>
            </Link>
          );
        })}
      </div>
    </section>
  );
}

function RightPanel() {
  return (
    <aside className="space-y-5">
      <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-5 backdrop-blur">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-black text-white">
            Recommended Products
          </h3>
          <Link href="/market-analysis" className="text-sm text-fuchsia-400">
            See all⌄
          </Link>
        </div>

        <div className="mt-5 space-y-4">
          {recommendedProducts.map((item, index) => (
            <Link
              href="/product-validation"
              key={item.name}
              className="flex items-center gap-4 rounded-xl p-2 transition hover:bg-white/[0.04]"
            >
              <div className="flex h-14 w-14 items-center justify-center rounded-xl bg-gradient-to-br from-slate-200 to-slate-600 text-slate-950">
                {index === 0 ? (
                  <PackageCheck />
                ) : index === 1 ? (
                  <Bot />
                ) : index === 2 ? (
                  <Sparkles />
                ) : (
                  <FileText />
                )}
              </div>

              <div className="min-w-0 flex-1">
                <p className="truncate font-bold text-white">{item.name}</p>
                <p className="truncate text-sm text-slate-400">
                  {item.detail}
                </p>
              </div>

              <span className="rounded-lg border border-emerald-500/40 bg-emerald-500/10 px-3 py-2 text-sm font-bold text-emerald-400">
                {item.score}
              </span>
            </Link>
          ))}
        </div>
      </div>

      <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-5 backdrop-blur">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-black text-white">
            Next 7 Days Action Plan
          </h3>
          <Link
            href="/seven-agent-dashboard"
            className="text-sm text-fuchsia-400"
          >
            View all⌄
          </Link>
        </div>

        <div className="mt-5 space-y-4">
          {actionPlan.map((item, index) => {
            const stepColor =
              index < 2
                ? "bg-violet-600"
                : index === 2
                  ? "bg-amber-500"
                  : "bg-orange-500";

            return (
              <div
                key={item.title}
                className="flex items-center gap-4 border-b border-white/5 pb-4 last:border-0 last:pb-0"
              >
                <div
                  className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-full ${stepColor}`}
                >
                  <ClipboardList size={17} />
                </div>

                <p className="flex-1 text-sm text-slate-200">{item.title}</p>
                <p className="text-xs text-slate-500">{item.due}</p>
              </div>
            );
          })}
        </div>
      </div>

      <div className="relative overflow-hidden rounded-2xl border border-fuchsia-500/30 bg-gradient-to-br from-violet-950 to-slate-900 p-5">
        <div className="absolute -right-5 bottom-0 h-28 w-28 rotate-12 rounded-2xl border border-fuchsia-500/30 bg-slate-950/60" />

        <h3 className="text-lg font-black text-white">
          Your AI-Powered Report is Ready!
        </h3>

        <p className="mt-4 max-w-xs text-sm leading-6 text-slate-300">
          Get the full breakdown of your business strategy, insights, and next
          steps.
        </p>

        <Link
          href="/reports"
          className="mt-6 inline-flex items-center gap-3 rounded-xl bg-gradient-to-r from-fuchsia-500 to-orange-500 px-6 py-3 text-sm font-bold text-white transition hover:opacity-90"
        >
          Download Report
          <Download size={17} />
        </Link>
      </div>
    </aside>
  );
}

function ChartsSection() {
  return (
    <section className="grid gap-5 xl:grid-cols-[1.4fr_1fr]">
      <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-5 backdrop-blur">
        <div className="flex items-center justify-between">
          <h3 className="font-black text-white">Opportunity Trend</h3>

          <span className="rounded-lg border border-white/10 px-3 py-1 text-xs text-slate-400">
            Last 6 Weeks⌄
          </span>
        </div>

        <div className="mt-5 flex h-44 items-end gap-3 border-b border-l border-white/10 px-4">
          {[38, 52, 40, 55, 48, 72, 60, 85, 78, 100].map(
            (height, index) => (
              <div
                key={index}
                className="flex flex-1 flex-col items-center gap-2"
              >
                <div
                  style={{ height }}
                  className="w-full rounded-t-xl bg-gradient-to-t from-orange-500/50 to-violet-500"
                />
              </div>
            ),
          )}
        </div>
      </div>

      <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-5 backdrop-blur">
        <h3 className="font-black text-white">Score Breakdown</h3>

        <div className="mt-6 flex flex-col items-center justify-center gap-5 md:flex-row">
          <div className="flex h-36 w-36 items-center justify-center rounded-full bg-[conic-gradient(#8b5cf6_0_24%,#ec4899_24%_44%,#f97316_44%_72%,#f59e0b_72%_100%)] p-4">
            <div className="flex h-full w-full flex-col items-center justify-center rounded-full bg-[#0c1428]">
              <p className="text-4xl font-black">83</p>
              <p className="text-xs text-slate-400">/100</p>
            </div>
          </div>

          <div className="space-y-3 text-sm">
            <p>
              <span className="text-violet-400">■</span> Business Readiness{" "}
              <span className="ml-8 text-slate-300">24%</span>
            </p>
            <p>
              <span className="text-pink-500">■</span> Product Fit{" "}
              <span className="ml-20 text-slate-300">20%</span>
            </p>
            <p>
              <span className="text-orange-500">■</span> Market Match{" "}
              <span className="ml-14 text-slate-300">28%</span>
            </p>
            <p>
              <span className="text-amber-400">■</span> Validation Score{" "}
              <span className="ml-10 text-slate-300">28%</span>
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}

export default function DashboardPage() {
  return (
    <main className="min-h-screen bg-[#030816] text-white">
      <div className="flex">
        <Sidebar />

        <section className="min-w-0 flex-1 p-5 lg:p-7">
          <Topbar />

          <LiveSystemStatus />

          <div className="mt-6 grid gap-6 xl:grid-cols-[1fr_390px]">
            <div className="space-y-5">
              <HeroBanner />
              <DashboardShortcuts />
              <ScoreCards />
              <AgentDashboard />
              <ChartsSection />
            </div>

            <RightPanel />
          </div>
        </section>
      </div>
    </main>
  );
}





