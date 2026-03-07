/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                primary: "#0ea5e9", // Vivid bright blue
                secondary: "#f1f5f9", // Light background for tabs
                background: "#F8FAFC", // Very light gray-blue background
                surface: "#FFFFFF", // White cards
                textMain: "#0f172a", // Dark slate for better readability
                textMuted: "#64748b", // Soft slate
                success: "#10b981",
                danger: "#ef4444",
                warning: "#f59e0b"
            }
        },
    },
    plugins: [],
}
