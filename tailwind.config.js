/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'electric-green': '#9AFF00',
        'bright-cyan': '#00FFFF',
        'error-gray': '#6B7280',
        'warning-white': '#F9FAFB',
      },
      backgroundImage: {
        'primary-gradient': 'linear-gradient(135deg, #9AFF00 0%, #00FFFF 100%)',
        'secondary-gradient': 'linear-gradient(135deg, #00FFFF 0%, #9AFF00 100%)',
        'dark-gradient': 'linear-gradient(135deg, #1a1a2e 0%, #2d3748 100%)',
        'app-gradient': 'linear-gradient(135deg, #1a1a2e 0%, #2d3748 100%)',
      },
    },
  },
  plugins: [],
}