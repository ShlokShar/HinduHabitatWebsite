/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/*"],
  theme: {
    extend: {
      colors: {
        "primary": "#6E4C04",
        "secondary": "#F7D785",
        "accent": "#FFB903"
      },
      fontFamily: {
        "ubuntu": ["Ubuntu"],
        "inter": ["Inter"],
      }
    },
  },
  plugins: [],
}

