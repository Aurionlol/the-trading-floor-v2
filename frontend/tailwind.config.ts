import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--bg-primary)",
        "bg-elevated": "var(--bg-elevated)",
        card: "var(--bg-card)",
        
        "gold-primary": "var(--gold-primary)",
        "gold-muted": "var(--gold-muted)",
        "gold-bright": "var(--gold-bright)",
        
        "green-banker": "var(--green-banker)",
        "orange-warning": "var(--orange-warning)",
        
        "text-primary": "var(--text-primary)",
        "text-secondary": "var(--text-secondary)",
        "text-muted": "var(--text-muted)",
      },
      fontFamily: {
        headline: ["var(--font-bebas)", "sans-serif"],
        mono: ["var(--font-mono)", "monospace"],
        serif: ["var(--font-serif)", "serif"],
      },
      animation: {
        "pulse-amber": "pulse-amber 2s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "slide-in": "slide-in 0.3s cubic-bezier(0.4, 0, 0.2, 1) forwards",
        "fill-gold": "fill-gold 0.3s ease-out forwards",
      },
      keyframes: {
        "pulse-amber": {
          "0%, 100%": { opacity: "1", boxShadow: "0 0 5px var(--gold-muted)" },
          "50%": { opacity: ".8", boxShadow: "0 0 15px var(--gold-primary)" },
        },
        "slide-in": {
          "0%": { transform: "translateX(-10px)", opacity: "0" },
          "100%": { transform: "translateX(0)", opacity: "1" },
        },
        "fill-gold": {
          "0%": { width: "0%" },
          "100%": { width: "100%" },
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
};
export default config;
