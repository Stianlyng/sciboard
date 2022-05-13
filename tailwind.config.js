module.exports = {
    content: ["./app/templates/main/frontpage.html",
        "./src/**/*.{html,js}",
        "./app/static/**/*.{html,js}",
        "./app/**/*.{html,js}",
    "./app/templates/**/*.{html,js}",
        "./app/templates/components/**/*.{html,js}",
    ],
    theme: {
        extend: {},
    },
    plugins: [require('@tailwindcss/line-clamp'),require('@tailwindcss/forms'),],
}

// npm install -D tailwindcss
// npx tailwindcss init
// npm install -D @tailwindcss/line-clamp
// npm install -D @tailwindcss/forms
// npx tailwindcss -i ./src/input.css -o ./app/static/css/tailwinds-output.css --watch
