/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/*"],
  theme: {
    extend: {
      colors: {
        "primary": "#6E4B04",
        "secondary": "#FFF4DD",
        "accent": "#FEB902"
      },
      fontFamily: {
        "poppins": ["Poppins"],
      }
    },
  },
  plugins: [],
}

