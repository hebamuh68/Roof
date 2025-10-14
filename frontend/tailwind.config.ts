import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        'poppins': ['Poppins', 'sans-serif'],
        'inter': ['Inter', 'sans-serif'],
      },
      colors: {
        // Design System Colors
        'orange': '#FF8C42', // Muted light orange
        'green': '#2D5016', // Medium to dark olive green
        'light-gn': '#E8F5E8', // Very light pastel green
        'dark-bl': '#000000', // Solid black
        'white': '#FFFFFF', // White
        // Additional brand colors
        'secondary': {
          DEFAULT: '#E8F5E8',
          100: '#D1EBD1',
          200: '#A3D7A3',
          300: '#75C375',
          400: '#4BC974',
          500: '#00A060',
          600: '#008A51',
          700: '#007342',
          800: '#005C33',
          900: '#004524',
        },
        'primary': {
          DEFAULT: '#FFF4E6',
          100: '#FFE9CC',
          200: '#FFD399',
          300: '#FFBD66',
          400: '#FFA733',
          500: '#FF8C42',
          600: '#E67A3A',
          700: '#CC6832',
          800: '#B3562A',
          900: '#994422',
        }
      },
      fontSize: {
        '4xl': ['100px', { lineHeight: 'auto' }],
        '3xl': ['48px', { lineHeight: 'auto' }],
        '2xl': ['32px', { lineHeight: 'auto' }],
        'xl': ['25px', { lineHeight: 'auto' }],
        'base': ['18px', { lineHeight: 'auto' }],
      }
    },
  },
  plugins: [],
}

export default config
