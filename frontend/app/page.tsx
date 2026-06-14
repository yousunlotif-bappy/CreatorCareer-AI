import Link from "next/link";

export default function HomePage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-[#030816] p-6 text-white">
      {/* 
        Landing Page Card
        This is the first screen users will see before entering the dashboard.
        It gives a quick idea about what CreatorCareer AI does.
      */}
      <section className="max-w-2xl rounded-3xl border border-white/10 bg-[#0c1428] p-10 text-center shadow-[0_0_45px_rgba(168,85,247,0.2)]">
        {/* Project name / small label */}
        <p className="text-sm font-bold uppercase tracking-[0.3em] text-fuchsia-400">
          CreatorCareer AI
        </p>

        {/* Main headline */}
        <h1 className="mt-5 text-4xl font-black leading-tight md:text-6xl">
          From Content Creator to Digital Entrepreneur
        </h1>

        {/* Short explanation of the product */}
        <p className="mt-5 leading-7 text-slate-400">
          CreatorCareer AI helps creators turn their content, audience, and
          skills into real business opportunities. It supports product
          validation, market analysis, ethical monetization, 7-agent planning,
          and downloadable business roadmap reports.
        </p>

        {/* Main call-to-action button */}
        <Link
          href="/dashboard"
          className="mt-8 inline-flex rounded-xl bg-gradient-to-r from-orange-500 to-fuchsia-600 px-7 py-3 font-bold text-white transition hover:scale-105 hover:opacity-95"
        >
          Open Dashboard
        </Link>
      </section>
    </main>
  );
}


