/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./lib/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        // Base palette — dark command-centre
        base: {
          900: "#060a13",
          800: "#0b0f1a",
          700: "#0e131f",
          600: "#141a2b",
          500: "#1a2236",
          400: "#232c42",
          300: "#2e3a54",
        },
        // Text
        slate: {
          100: "#e8ecf4",
          200: "#c7d0e0",
          300: "#a0aec0",
          400: "#8a94a6",
          500: "#6b7588",
        },
        // Risk levels
        risk: {
          critical: "#ff2e63",
          high: "#ff7f0e",
          medium: "#f4c430",
          low: "#2ecc71",
        },
        // Accent / node types
        accent: {
          blue: "#4da6ff",
          purple: "#a66bff",
          cyan: "#00d0d0",
          green: "#2ecc71",
          orange: "#ff7f0e",
          pink: "#ff2e63",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "-apple-system", "sans-serif"],
        mono: ["JetBrains Mono", "Fira Code", "monospace"],
      },
      borderRadius: {
        xl: "14px",
        "2xl": "18px",
      },
      boxShadow: {
        glow: "0 0 20px rgba(77, 166, 255, 0.15)",
        "glow-red": "0 0 20px rgba(255, 46, 99, 0.2)",
        "glow-green": "0 0 20px rgba(46, 204, 113, 0.2)",
        "glow-orange": "0 0 20px rgba(255, 127, 14, 0.2)",
        card: "0 4px 24px rgba(0, 0, 0, 0.3)",
      },
      animation: {
        "pulse-slow": "pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "fade-in": "fadeIn 0.5s ease-out",
        "slide-up": "slideUp 0.4s ease-out",
        "slide-in-right": "slideInRight 0.3s ease-out",
        glow: "glowPulse 2s ease-in-out infinite alternate",
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        slideUp: {
          "0%": { opacity: "0", transform: "translateY(16px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        slideInRight: {
          "0%": { opacity: "0", transform: "translateX(20px)" },
          "100%": { opacity: "1", transform: "translateX(0)" },
        },
        glowPulse: {
          "0%": { boxShadow: "0 0 8px rgba(77, 166, 255, 0.1)" },
          "100%": { boxShadow: "0 0 20px rgba(77, 166, 255, 0.25)" },
        },
      },
    },
  },
  plugins: [],
};
