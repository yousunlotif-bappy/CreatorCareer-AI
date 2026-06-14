import axios from "axios";

/*
  API_BASE_URL is the backend server address.

  During local development:
  - Frontend runs on http://localhost:3000
  - Backend runs on http://localhost:8000

  Later, when we deploy the backend online, we can change this URL
  from .env.local without touching the code.
*/
export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

/*
  This axios instance will be used across the frontend
  whenever we need to talk with the FastAPI backend.
*/
export const api = axios.create({
  baseURL: API_BASE_URL,
});


