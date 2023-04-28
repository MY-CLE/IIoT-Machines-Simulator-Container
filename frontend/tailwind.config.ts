/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}", "./ts/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        "header-red": "#9C162B",
      },
    },
  },
  plugins: [],
};
