<template>
  <LMap class="min-h-[calc(100vh-var(--header-height))]" style="display: flex; height: 100%;" :zoom="6" :center="[47.21322, -1.559482]">
    <LTileLayer
      url="https://tile.openstreetmap.de/{z}/{x}/{y}.png"
      attribution='&amp;copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
      layer-type="base"
      name="OpenStreetMap"
    />
    <LMarker v-for="waypoint in waypoints" :key="waypoint.lat + waypoint.lng" :lat-lng="[waypoint.lat, waypoint.lng]">
      <LTooltip> Hi! I'm staying here on this location! </LTooltip>
    </LMarker>
  </LMap>
</template>
<script setup lang="ts">
const waypoints = [
  { lat: 38.7436056, lng: -9.2304153 },
  { lat: 38.7436056, lng: -0.131281 },
];
</script>