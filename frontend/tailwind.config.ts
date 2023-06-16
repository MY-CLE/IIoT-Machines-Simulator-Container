/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}", "./ts/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        "header-red": "#9C162B",
        "button-blue": "#2A8C75",
        "selectedbar-green": "#80C7B6",
        "unselectedbar-green": "#2A8C75",
        "program-choose-grey": "#354970",
      },
      backgroundImage: {
        "lasercuter-img": "url('../images/ventis_AJ_amada_Lasercutter.png')",
      },
      width: {
        '1/10': '10%',
        '1/6': '16%',
        '3/10': '30%',
        '3/20': '15%',
        '1/16': '6%',
      },
    },
  },
  plugins: [],
};
