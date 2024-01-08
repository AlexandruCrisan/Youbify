/** @type {import('tailwindcss').Config} */
const defaultTheme = require("tailwindcss/defaultTheme");

module.exports = {
    content: ["./templates/*.html"],
    theme: {
        extend: {
            fontFamily: {
                dm_sans: ["DM Sans", ...defaultTheme.fontFamily.sans],
                rubik: ["Rubik", ...defaultTheme.fontFamily.sans],
                satisfy: ["Satisfy", ...defaultTheme.fontFamily.sans]
            },
            colors: {
                midnightsky: "#001220",
                youtube: "#B41313",
                spotify: "#1DB954"
            },
            screens: {
                "3xl": "2000px"
            },
            backgroundImage: {
                spotify_logo: "url('/static/img/spotify_logo.svg')"
            }
        }
    },
    plugins: []
};

