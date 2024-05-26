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
