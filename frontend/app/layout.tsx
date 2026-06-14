import type { Metadata } from "next";
import "./globals.css";

/*
  CreatorCareer AI - Global Metadata

  This metadata controls how the project appears in:
  - Browser tabs
  - Search engines
  - Social media previews
  - Open Graph previews
  - Twitter/X cards

  CreatorCareer AI is positioned as a creator business operating system.
  The project workflow was planned and structured with support from IBM Bob,
  while the AI-powered business logic is designed around IBM Granite / watsonx-style intelligence.
*/

export const metadata: Metadata = {
  title: {
    default: "CreatorCareer AI | Creator Business OS",
    template: "%s | CreatorCareer AI",
  },

  description:
    "CreatorCareer AI is an AI-powered creator business operating system that helps content creators move from content ideas to market opportunity, product validation, ethical monetization, 7-agent business strategy, PDF reporting, and saved business history.",

  keywords: [
    "CreatorCareer AI",
    "creator business operating system",
    "AI creator dashboard",
    "AI content generation",
    "creator economy",
    "product validation",
    "ethical monetization",
    "affiliate roadmap",
    "dropshipping roadmap",
    "7-agent AI dashboard",
    "IBM Bob",
    "IBM Granite",
    "watsonx AI",
    "FastAPI",
    "Next.js",
    "Supabase",
  ],

  authors: [{ name: "CreatorCareer AI Team" }],
  creator: "CreatorCareer AI Team",
  publisher: "CreatorCareer AI",

  /*
    Open Graph metadata helps the project look professional
    when shared on platforms like LinkedIn, Facebook, Discord, and Messenger.
  */
  openGraph: {
    title: "CreatorCareer AI | Creator Business OS",
    description:
      "An AI-powered platform that helps creators turn content into validated, ethical, and structured digital business roadmaps.",
    url: "https://creator-career-ai.vercel.app",
    siteName: "CreatorCareer AI",
    type: "website",
    locale: "en_US",
  },

  /*
    Twitter/X preview metadata.
    This gives the project a strong social preview when shared online.
  */
  twitter: {
    card: "summary_large_image",
    title: "CreatorCareer AI | Creator Business OS",
    description:
      "From content creator to digital entrepreneur — supported by IBM Bob-inspired planning, AI workflow, product validation, ethical monetization, and 7-agent business strategy.",
  },

  icons: {
    icon: "/favicon.ico",
  },
};

/*
  RootLayout is the main layout wrapper for the full Next.js application.
  Every page of CreatorCareer AI will be rendered inside this layout.

  The language is set to English because the project is built for a global
  creator economy audience, including creators, startup judges, and AI challenge reviewers.
*/

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}


