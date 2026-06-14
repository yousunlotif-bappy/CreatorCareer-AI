/*
  Dashboard Demo Data
  -------------------
  This file contains static data for the dashboard UI.

  Later, these values can come from:
  - FastAPI backend
  - IBM Granite / watsonx AI response
  - Supabase database
  - User profile analysis
*/

/*
  Score cards show the main creator business performance indicators.
  These are demo values for the UI prototype.
*/
export const scoreCards = [
  {
    title: "Business Readiness",
    value: 82,
    suffix: "/100",
    growth: "+12%",
    status: "Strong",
    color: "purple",
  },
  {
    title: "Product Fit",
    value: 78,
    suffix: "/100",
    growth: "+8%",
    status: "Good",
    color: "pink",
  },
  {
    title: "Market Match",
    value: 86,
    suffix: "/100",
    growth: "+14%",
    status: "Excellent",
    color: "orange",
  },
  {
    title: "Validation Score",
    value: 88,
    suffix: "/100",
    growth: "+16%",
    status: "Excellent",
    color: "amber",
  },
];

/*
  AI business modules
  -------------------
  The first 7 cards represent the main AI agent workflow.
  The last card adds Affiliate & Dropshipping strategy so the Day 2 UI
  clearly shows this important monetization feature.
*/
export const agentCards = [
  {
    title: "Business Readiness",
    description: "Evaluates the creator's business foundation and readiness.",
    accent: "purple",
  },
  {
    title: "Niche-to-Product Fit",
    description:
      "Finds suitable digital product ideas based on the creator's niche.",
    accent: "pink",
  },
  {
    title: "Audience-to-Market Matching",
    description: "Matches the creator's audience with real market demand.",
    accent: "orange",
  },
  {
    title: "Content-to-Commerce Roadmap",
    description: "Turns content strategy into a practical business roadmap.",
    accent: "orange",
  },
  {
    title: "Ethical Monetization Check",
    description:
      "Checks transparency, trust, compliance, and responsible monetization.",
    accent: "amber",
  },
  {
    title: "Product Validation",
    description:
      "Validates product ideas using demand, competition, and user interest.",
    accent: "purple",
  },
  {
    title: "6-Month Roadmap",
    description: "Creates a step-by-step growth plan for the next six months.",
    accent: "pink",
  },
  {
    title: "Affiliate & Dropshipping Strategy",
    description:
      "Suggests affiliate, dropshipping, and low-risk monetization ideas for creators.",
    accent: "amber",
  },
];

/*
  Recommended Products
  --------------------
  These are sample AI-recommended product opportunities.
  They help show how the dashboard converts content ideas into business ideas.
*/
export const recommendedProducts = [
  {
    name: "AI Content Planner",
    detail: "High demand • Low competition",
    score: "92%",
  },
  {
    name: "Digital Creator Toolkit",
    detail: "High demand • Medium competition",
    score: "88%",
  },
  {
    name: "Faceless YouTube System",
    detail: "High demand • Low competition",
    score: "85%",
  },
  {
    name: "Affiliate Product Finder",
    detail: "High demand • Low startup cost",
    score: "82%",
  },
];

/*
  Next 7 Days Action Plan
  -----------------------
  This plan helps creators move from analysis to execution.
*/
export const actionPlan = [
  {
    title: "Validate product idea with audience poll",
    due: "Due in 1 day",
  },
  {
    title: "Analyze competitors and pricing",
    due: "Due in 2 days",
  },
  {
    title: "Create content-to-commerce roadmap",
    due: "Due in 3 days",
  },
  {
    title: "Research affiliate and dropshipping product options",
    due: "Due in 4 days",
  },
  {
    title: "Build MVP or first product draft",
    due: "Due in 5 days",
  },
  {
    title: "Plan launch content and pre-sell strategy",
    due: "Due in 7 days",
  },
];


