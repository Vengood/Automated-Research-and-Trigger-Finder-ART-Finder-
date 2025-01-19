/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        
        Gilroy: ['Gilroy-Regular', 'sans-serif'], // Adding your own custom font
      },
    },
  },
  plugins: [],
}

