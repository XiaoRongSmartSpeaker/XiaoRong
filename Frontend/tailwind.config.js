module.exports = {
  purge: [],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
        primary: '#FF6363',
        secondary: {
          100: '#E2E2D5',
          200: '#888883',
        },
        theme: '#415765',
        light_theme: '#92A7B0',
        dark_theme: '#2E434E',
        normal_theme: '#587285'
      },
      fontSize: {
        xxs: ['0.65rem', { lineHeight: '0.875remr' }],
      }
    },
    fontFamily: {
      body: ['Nunito'],
    }
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
