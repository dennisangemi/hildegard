/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './docs/**/*.{html,js,md}',
    './overrides/**/*.html'
  ],
  corePlugins: {
    preflight: false, // Disabilita il reset CSS di Tailwind per evitare conflitti con MkDocs Material
  },
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f4f5',
          100: '#d1dde1',
          200: '#b3c7cc',
          300: '#94b0b8',
          400: '#759aa3',
          500: '#607d84',
          600: '#4c6369',
          700: '#37484d',
          800: '#233032',
          900: '#0f1516'
        },
        accent: {
          50: '#e0f7f6',
          100: '#b3ebe8',
          200: '#80dfda',
          300: '#4dd3cb',
          400: '#26c6bd',
          500: '#00b8af',
          600: '#00948c',
          700: '#007069',
          800: '#004c46',
          900: '#002523'
        }
      },
      fontFamily: {
        sans: ['Poppins', 'sans-serif']
      }
    },
  },
  plugins: [],
}
