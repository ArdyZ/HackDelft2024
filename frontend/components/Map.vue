<template>
  <LMap
    class="min-h-[calc(100vh-var(--header-height))]"
    style="display: flex; height: 100%"
    :zoom="12"
    :center="[51.998752, 4.373719]"
    ref="map"
  >
    <LTileLayer
      url="https://tile.openstreetmap.de/{z}/{x}/{y}.png"
      attribution='&amp;copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
      layer-type="base"
      name="OpenStreetMap"
    />
    <LMarker
      v-for="member in members"
      :key="member.id"
      :lat-lng="[
        member.address.coordinates.latitude,
        member.address.coordinates.longitude,
      ]"
    >
      <LTooltip>{{ member.name }} | {{ member.address.name }}</LTooltip>
    </LMarker>
    <LPolyline :lat-lngs="routeCoords" color="red" />
  </LMap>

  <UCard class="absolute top-24 right-4 h-2/3 w-80 z-[9999]">
    <template #header>
      <h3
        class="text-base font-semibold leading-6 text-gray-900 dark:text-white"
      >
        Mission Control
      </h3>
    </template>

    <Placeholder class="h-full" />

    <template #footer>
      <UButton block icon="i-heroicons-rocket-launch">Run</UButton>
    </template>
  </UCard>
</template>

<script setup lang="ts">
const { data: members } = await useFetch("/api/member");
const { data: route } = await useFetch("/api/distance?a=26&b=22");

const routeCoords = computed(() =>
  route.value
    ? route.value.geometry.map((coord) => ({
        lat: coord.latitude,
        lng: coord.longitude,
      }))
    : []
);
</script>
