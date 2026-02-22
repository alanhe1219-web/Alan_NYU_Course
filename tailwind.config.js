/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        serif: ["var(--font-cormorant)", "serif"],
        sans: ["var(--font-outfit)", "sans-serif"],
      },
      colors: {
        nyu: {
          light: "#7B2BB5",
          DEFAULT: "#57068c",
          dark: "#330055",
        }
      }
    },
  },
  plugins: [],
}

