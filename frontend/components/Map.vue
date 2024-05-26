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
    <LMarker :lat-lng="[startLatitude, startLongitude]">
      <LTooltip>EEMCS</LTooltip>
    </LMarker>
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
    <LPolyline v-for="route in routeCoords" :lat-lngs="route" color="red" />
    <LPolyline v-for="route in routeCoords2" :lat-lngs="route" color="blue" />
  </LMap>

  <UCard class="absolute top-24 right-4 w-80 z-[9999]">
    <template #header>
      <h3
        class="text-base font-semibold leading-6 text-gray-900 dark:text-white"
      >
        Mission Control
      </h3>
    </template>

    <UFormGroup label="Cars Available" name="carsAvailable" class="mb-2">
      <UInput
        v-model="state.cars.available"
        type="number"
        icon="i-material-symbols-directions-car"
      />
    </UFormGroup>

    <UFormGroup label="Bikes Available" name="bikesAvailable" class="mb-2">
      <UInput
        v-model="state.bikes.available"
        type="number"
        icon="i-material-symbols-directions-bike"
      />
    </UFormGroup>

    <UFormGroup label="Capacity per Bike" name="bikesCapacity" class="mb-2">
      <UInput
        v-model="state.bikes.capacity"
        type="number"
        icon="i-material-symbols-backpack"
      />
    </UFormGroup>

    <template #footer>
      <UButton block icon="i-heroicons-rocket-launch">Run</UButton>
    </template>
  </UCard>
</template>

<script setup lang="ts">
import {
  longitude as startLongitude,
  latitude as startLatitude,
} from "../server/lib/start";

const { data: members } = await useFetch("/api/member");
const { data: route1 } = await useFetch("/api/distance?a=17&b=19&type=driving");
const { data: route2 } = await useFetch("/api/distance?a=19&b=24&type=driving");
const { data: route3 } = await useFetch("/api/distance?a=19&b=24&type=cycling");

const routeCoords = computed(() => {
    const routes = [route1, route2]
    return routes.map((route) =>
      route.value
        ? route.value.geometry.map((coord) => ({
          lat: coord.latitude,
          lng: coord.longitude,
        }))
        : []
    )
  }
);

const routeCoords2 = computed(() => {
    const routes = [route3]
    return routes.map((route) =>
      route.value
        ? route.value.geometry.map((coord) => ({
          lat: coord.latitude,
          lng: coord.longitude,
        }))
        : []
    )
  }
);

const state = reactive({
  cars: {
    available: 1,
  },
  bikes: {
    available: 4,
    capacity: 20,
  },
});
</script>
