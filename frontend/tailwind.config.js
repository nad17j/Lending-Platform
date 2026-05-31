/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        banking: {
          navy: '#0f172a',    // Slate 900
          gold: '#b45309',    // Amber 700
          emerald: '#047857' // Emerald 700
        }
      }
    },
  },
  plugins: [],
}