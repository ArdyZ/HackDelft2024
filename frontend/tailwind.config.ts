import type { Config } from "tailwindcss";

export default <Partial<Config>>{
  theme: {
    extend: {
      colors: {
        indigo: {
          "50": "#eef8ff",
          "100": "#dcf0ff",
          "200": "#b2e3ff",
          "300": "#6dceff",
          "400": "#20b6ff",
          "500": "#009cff",
          "600": "#007cdf",
          "700": "#0062b4",
          "800": "#005395",
          "900": "#00447a",
          "950": "#00274a",
        },
      },
    },
  },
};
