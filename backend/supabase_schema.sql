-- CreatorCareer AI Supabase Schema
-- Run this in Supabase SQL Editor if tables or columns are missing.

create extension if not exists "pgcrypto";

create table if not exists creators (
  id uuid primary key default gen_random_uuid(),
  name text,
  niche text,
  platforms jsonb,
  followers int,
  audience text,
  region text,
  skills text,
  business_interest text,
  income_goal text,
  available_time text,
  current_challenge text,
  readiness_score int,
  creator_stage text,
  created_at timestamptz default now()
);

create table if not exists content_outputs (
  id uuid primary key default gen_random_uuid(),
  creator_id uuid null,
  topic text,
  platform text,
  audience text,
  tone text,
  duration text,
  language text,
  content_goal text,
  titles jsonb,
  hook text,
  voiceover_script text,
  caption text,
  hashtags jsonb,
  thumbnail_text jsonb,
  cta text,
  platform_notes text,
  scene_breakdown jsonb,
  video_generation_prompt text,
  b_roll_ideas jsonb,
  editing_notes jsonb,
  created_at timestamptz default now()
);

create table if not exists market_analysis_results (
  id uuid primary key default gen_random_uuid(),
  creator_id uuid null,
  niche text,
  audience text,
  region text,
  platforms jsonb,
  business_type text,
  budget text,
  product_interest text,
  matched_category text,
  market_summary text,
  demand_level text,
  competition_level text,
  recommended_products jsonb,
  digital_product_ideas jsonb,
  affiliate_product_ideas jsonb,
  dropshipping_product_ideas jsonb,
  best_platforms jsonb,
  risk_level text,
  opportunity_score int,
  business_type_note text,
  next_best_action text,
  data_note text,
  created_at timestamptz default now()
);

create table if not exists product_scores (
  id uuid primary key default gen_random_uuid(),
  creator_id uuid null,
  product_name text,
  niche text,
  audience text,
  region text,
  platform text,
  business_model text,
  budget text,
  product_type text,
  promotion_style text,
  audience_fit_score int,
  market_demand_score int,
  competition_score int,
  content_promotion_fit_score int,
  profit_potential_score int,
  ease_of_starting_score int,
  total_score int,
  status text,
  recommendation text,
  strengths jsonb,
  risks jsonb,
  validation_checklist jsonb,
  next_best_action text,
  data_note text,
  created_at timestamptz default now()
);

create table if not exists affiliate_roadmaps (
  id uuid primary key default gen_random_uuid(),
  creator_id uuid null,
  niche text,
  audience text,
  region text,
  platforms jsonb,
  business_type text,
  budget text,
  product_category text,
  content_style text,
  roadmap_summary text,
  affiliate_product_ideas jsonb,
  dropshipping_product_ideas jsonb,
  best_product_fit text,
  content_promotion_plan jsonb,
  supplier_research_checklist jsonb,
  thirty_day_roadmap jsonb,
  risk_analysis jsonb,
  ethical_disclosure text,
  next_best_action text,
  data_note text,
  created_at timestamptz default now()
);

create table if not exists ethical_check_results (
  id uuid primary key default gen_random_uuid(),
  creator_id uuid null,
  content_text text,
  platform text,
  promotion_type text,
  has_affiliate_link boolean,
  product_claim text,
  target_audience text,
  ethical_score int,
  risk_level text,
  issues_found jsonb,
  disclosure_status text,
  safer_version text,
  recommended_disclosure text,
  next_best_action text,
  platform_note text,
  data_note text,
  created_at timestamptz default now()
);

create table if not exists seven_agent_reports (
  id uuid primary key default gen_random_uuid(),
  creator_id uuid null,
  creator_niche text,
  audience text,
  region text,
  platforms jsonb,
  followers int,
  product_idea text,
  business_model text,
  income_goal text,
  available_time text,
  promotion_copy text,
  overall_business_opportunity_score int,
  executive_summary text,
  agent_results jsonb,
  next_7_days_plan jsonb,
  score_weights jsonb,
  data_note text,
  created_at timestamptz default now()
);

create table if not exists reports (
  id uuid primary key default gen_random_uuid(),
  creator_id uuid null,
  creator_name text,
  creator_niche text,
  audience text,
  region text,
  platforms jsonb,
  product_idea text,
  business_model text,
  income_goal text,
  overall_business_opportunity_score int,
  report_file_name text,
  report_download_url text,
  created_at timestamptz default now()
);



