<template>
  <LMap
      class="min-h-[calc(100vh-var(--header-height))]"
      style="display: flex; height: 100%;" :zoom="6" :center="[47.21322, -1.559482]"
      ref="map"
  >
    <LTileLayer
      url="https://tile.openstreetmap.de/{z}/{x}/{y}.png"
      attribution='&amp;copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
      layer-type="base"
      name="OpenStreetMap"
    />
    <LMarker v-for="waypoint in waypoints" :key="waypoint.lat + waypoint.lng" :lat-lng="[waypoint.lat, waypoint.lng]" draggable>
      <LTooltip>{{waypoint.description}}</LTooltip>
    </LMarker>
  </LMap>
</template>
<script setup lang="ts">

const waypoints: {lat: number, lng: number, description: string}[] = [
  { lat: 38.7436056, lng: -9.2304153, description: "test1" },
  { lat: 38.7436056, lng: -0.131281, description: "test2" },
];
</script>
