export default defineNuxtConfig({
  app: {
    head: {
      charset: "utf-8",
      viewport: "width=device-width, initial-scale=1",
      link: [{ rel: "icon", type: "image/png", href: "/favicon.png" }],
    },
  },
  devtools: { enabled: true },
  extends: ["@nuxt/ui-pro"],
  modules: ["@nuxt/ui", "@nuxt/image", "nuxt3-leaflet"],
});
