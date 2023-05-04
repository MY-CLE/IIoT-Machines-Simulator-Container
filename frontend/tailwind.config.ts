/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}", "./ts/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        "header-red": "#9C162B",
        "button-blue": "#2A8C75",
      },
      backgroundImage: {
        "lasercuter-img": "url('../images/ventis_AJ_amada_Lasercutter.png')",
      },
    },
  },
  plugins: [],
};