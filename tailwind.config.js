/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        './templates/**/*.html',
        './node_modules/flowbite/**/*.js',
        './web_app/forms/css_classes/*.py',
        './static/**/*.js',
        './static/**/*.svg'
    ],
    plugins: [
        require('flowbite/plugin'),
    ],
    theme: {
        extend: {
            fontFamily: {
                sans: ['Lato', 'sans-serif'],
            },
            colors: {
                'atomic-tangerine': {
                    DEFAULT: '#ef946c',
                    900: '#3e1807',
                    800: '#7d2f0e',
                    700: '#bb4715',
                    600: '#e8662e',
                    500: '#ef946c',
                    400: '#f2a989',
                    300: '#f5bea7',
                    200: '#f8d4c4',
                    100: '#fce9e2'
                },
                'marian-blue': {
                    DEFAULT: '#1e3888',
                    900: '#060b1c',
                    800: '#0c1737',
                    700: '#122253',
                    600: '#182e6e',
                    500: '#1e3888',
                    400: '#2b50c2',
                    300: '#5778da',
                    200: '#8fa5e6',
                    100: '#c7d2f3'
                },
                'carmine': {
                    DEFAULT: '#9a031e',
                    900: '#1f0106',
                    800: '#3e010c',
                    700: '#5d0213',
                    600: '#7c0319',
                    500: '#9a031e',
                    400: '#e0052d',
                    300: '#fb3055',
                    200: '#fc758e',
                    100: '#febac6'
                },
                'cambridge-blue': {
                    DEFAULT: '#89bd9e',
                    900: '#182a1f',
                    800: '#2f543e',
                    700: '#477d5c',
                    600: '#60a57c',
                    500: '#89bd9e',
                    400: '#a1cab1',
                    300: '#b8d7c5',
                    200: '#d0e5d8',
                    100: '#e7f2ec'
                },
                'maize': {
                    DEFAULT: '#fce762',
                    900: '#453c01',
                    800: '#8a7803',
                    700: '#cfb404',
                    600: '#fadd1f',
                    500: '#fce762',
                    400: '#fcec83',
                    300: '#fdf1a2',
                    200: '#fef6c1',
                    100: '#fefae0'
                }
            },
            backgroundColor: {
                'red-300-40': 'rgba(248, 180, 180, 0.4)',
            }
        }
    }
}