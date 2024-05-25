<script setup lang="ts">
const links = [
  {
    label: "Start",
    icon: "i-heroicons-book-open",
    to: "/",
  },
  {
    label: "Releases",
    icon: "i-heroicons-rocket-launch",
    to: "/releases",
  },
  {
    label: "Members",
    icon: "i-heroicons-users-solid",
    to: "/members",
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
