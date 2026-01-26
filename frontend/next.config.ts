import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  env: {
    NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL || "https://hiba-05-todoapp-phase-2.hf.space",
  },
};

export default nextConfig;
