/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        './templates/**/*.html',
        './node_modules/flowbite/**/*.js',
        './web_app/forms/css_classes/*.py'
    ],
    plugins: [
        require('flowbite/plugin')
    ],
    theme: {
        extend: {
            fontFamily: {
                sans: ['Lato', 'sans-serif'],
            },
            colors: {
                'atomic-tangerine': {
                    DEFAULT: '#ef946c',
                    100: '#3e1807',
                    200: '#7d2f0e',
                    300: '#bb4715',
                    400: '#e8662e',
                    500: '#ef946c',
                    600: '#f2a989',
                    700: '#f5bea7',
                    800: '#f8d4c4',
                    900: '#fce9e2'
                },
                'marian-blue': {
                    DEFAULT: '#1e3888',
                    100: '#060b1c',
                    200: '#0c1737',
                    300: '#122253',
                    400: '#182e6e',
                    500: '#1e3888',
                    600: '#2b50c2',
                    700: '#5778da',
                    800: '#8fa5e6',
                    900: '#c7d2f3'
                },
                'carmine': {
                    DEFAULT: '#9a031e',
                    100: '#1f0106',
                    200: '#3e010c',
                    300: '#5d0213',
                    400: '#7c0319',
                    500: '#9a031e',
                    600: '#e0052d',
                    700: '#fb3055',
                    800: '#fc758e',
                    900: '#febac6'
                },
                'cambridge-blue': {
                    DEFAULT: '#89bd9e',
                    100: '#182a1f',
                    200: '#2f543e',
                    300: '#477d5c',
                    400: '#60a57c',
                    500: '#89bd9e',
                    600: '#a1cab1',
                    700: '#b8d7c5',
                    800: '#d0e5d8',
                    900: '#e7f2ec'
                },
                'maize': {
                    DEFAULT: '#fce762',
                    100: '#453c01',
                    200: '#8a7803',
                    300: '#cfb404',
                    400: '#fadd1f',
                    500: '#fce762',
                    600: '#fcec83',
                    700: '#fdf1a2',
                    800: '#fef6c1',
                    900: '#fefae0'
                }
            }
        },
    }
}