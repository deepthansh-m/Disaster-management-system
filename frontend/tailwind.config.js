module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      colors: {
        green: {
          50: '#f0fdf4',
          100: '#dcfce7',
          500: '#22c55e',
        },
        emerald: {
          500: '#10b981',
          600: '#059669',
          700: '#047857',
        },
      },
    },
  },
  plugins: [],
  important: true // This ensures Tailwind styles take precedence
}