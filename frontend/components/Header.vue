<script setup lang="ts">
const links = [
  {
    label: "Docs",
    icon: "i-heroicons-book-open",
    to: "/getting-started",
  },
  {
    label: "Pro",
    icon: "i-heroicons-square-3-stack-3d",
    to: "/pro",
  },
  {
    label: "Releases",
    icon: "i-heroicons-rocket-launch",
    to: "/releases",
  },
];
</script>

<template>
  <UHeader :links="links">
    <template #logo>
      <UColorModeImage
        class="w-auto h-8"
        light="/logos/indigo.png"
        dark="/logos/white.png"
      />
    </template>

    <template #right>
      <UColorModeButton />
    </template>

    <!-- <template #panel> -->
    <!-- <UNavigationTree :links="mapContentNavigation(navigation)" /> -->
    <!-- </template> -->
  </UHeader>
</template>
