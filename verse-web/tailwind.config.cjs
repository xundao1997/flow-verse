/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        canvas: '#f6f1e8',
        ink: '#17171c',
        ember: '#db6b44',
        lagoon: '#1f7a78',
        haze: '#efe7d7',
        cloud: '#fffdf8',
      },
      boxShadow: {
        panel: '0 24px 60px rgba(23, 23, 28, 0.08)',
      },
      borderRadius: {
        shell: '28px',
      },
      fontFamily: {
        display: ['Bahnschrift', 'Trebuchet MS', 'Segoe UI', 'sans-serif'],
        body: ['Segoe UI', 'Tahoma', 'Geneva', 'Verdana', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
