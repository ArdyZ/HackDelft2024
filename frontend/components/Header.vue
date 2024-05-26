<script setup lang="ts">
const links = [
  {
    label: "Members",
    icon: "i-heroicons-users-solid",
    to: "/members",
  },
  {
    label: "Map",
    icon: "i-heroicons-map",
    to: "/map",
  },
];
</script>

<template>
  <UHeader :links="links">
    <template #logo>
      <UColorModeImage
        class="w-auto h-8 max-sm:invisible"
        light="/logos/indigo.png"
        dark="/logos/white.png"
      />
    </template>

    <template #right>
      <UColorModeButton />
    </template>
  </UHeader>
</template>
