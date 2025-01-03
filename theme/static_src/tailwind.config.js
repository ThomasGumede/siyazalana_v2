/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
  content: [
    /**
     * HTML. Paths to Django template files that will contain Tailwind CSS classes.
     */

    /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
    "../templates/**/*.html",

    /*
     * Main templates directory of the project (BASE_DIR/templates).
     * Adjust the following line to match your project structure.
     */
    "../../templates/**/*.html",

    /*
     * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
     * Adjust the following line to match your project structure.
     */
    "../../**/templates/**/*.html",

    /**
     * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
     * patterns match your project structure.
     */
    /* JS 1: Ignore any JavaScript in node_modules folder. */
    // '!../../**/node_modules',
    /* JS 2: Process all JavaScript files in the project. */
    // '../../**/*.js',

    /**
     * Python: If you use Tailwind CSS classes in Python, uncomment the following line
     * and make sure the pattern below matches your project structure.
     */
    // '../../**/*.py'
  ],
  theme: {
    extend: {
      colors: {
        transparent: "transparent",
        current: "currentColor",
        "custom-primary": "#005a4a",
        "custom-secondary": "hsl(200, 69%, 14%)",
        "custom-text": "hsl(200, 15%, 43%)",
        "custom-bg": "hsl(225, 33%, 98%)",
        "custom-h": "hsl(188, 63%, 7%)",
        "custom-tertiary": "hsl(200, 15%, 43%)",
        "custom-text-2": "#bfbfc0",
        "primary-color": "#000000",
        "secondary-color": "#005a4a",
        "color-1": "#8cb2b2",
        "heading-color": "#071c1f",
        "paragraph-color": "#5c727d",
        
        "border-color-1": "#e5eaee",
        "section-bg-1": "#f2f6f7",
        "section-bg-2": "#171b2a",
        "border-color-9": "#e4ecf2",
        
      },
      fontFamily: {
        sans: ["Poppins", "sans-serif"],
        "heading-font": '"Poppins", sans-serif',
        "body-font": '"Nunito Sans", sans-serif',
      },
    },
    screens: {
      xs: "480px",

      sm: "576px",
      // => @media (min-width: 730px) { ... }

      md: "768px",
      // => @media (min-width: 1024px) { ... }

      lg: "992px",
      // => @media (min-width: 1204px) { ... }

      xl: "1200px",
      // => @media (min-width: 1440pxpx) { ... }

      xxl: "1300px",
      // => @media (min-width: 1636px) { ... }

      txxl: "1400px",

      dxxl: "1600px",
    },
  },
  plugins: [
    /**
     * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
     * for forms. If you don't like it or have own styling for forms,
     * comment the line below to disable '@tailwindcss/forms'.
     */
    // require("@tailwindcss/forms"),
    // require("@tailwindcss/typography"),
    // require("@tailwindcss/line-clamp"),
    require("@tailwindcss/aspect-ratio"),
  ],
};
