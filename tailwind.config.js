/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/**/*.js",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        background: 'rgb(var(--background))',
        card: 'rgb(var(--card))',
        border: 'rgb(var(--border))',
        accent: 'rgb(var(--accent))',
        'copy-primary': 'rgb(var(--copy-primary))',
        'copy-secondary': 'rgb(var(--copy-secondary))',
        cta: 'rgb(var(--cta))',
        'cta-active': 'rgb(var(--cta-active))',
        'cta-text': 'rgb(var(--cta-text))',
      },
    },
  },
  plugins: [],
}
