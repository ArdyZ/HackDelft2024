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
    <div v-for="(route, i) in currentWaypoints" :key="route.toString()">
      <LPolyline
        v-for="(e, j) in route"
        :key="j"
        :lat-lngs="e"
        :color="colors[i]"
      />
    </div>
  </LMap>

  <UForm
    ref="form"
    :schema="startSchema"
    :state="state"
    class="space-y-4"
    @submit="start"
  >
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
          v-model="state.carsAvailable"
          type="number"
          icon="i-material-symbols-directions-car"
        />
      </UFormGroup>

      <UFormGroup label="Bikes Available" name="bikesAvailable" class="mb-2">
        <UInput
          v-model="state.bikesAvailable"
          type="number"
          icon="i-material-symbols-directions-bike"
        />
      </UFormGroup>

      <UFormGroup label="Capacity per Bike" name="bikesCapacity" class="mb-2">
        <UInput
          v-model="state.bikesCapacity"
          type="number"
          icon="i-material-symbols-backpack"
        />
      </UFormGroup>

      <template #footer>
        <UButton type="submit" icon="i-heroicons-rocket-launch" block
          >Run</UButton
        >
      </template>
    </UCard>
  </UForm>
</template>

<script setup lang="ts">
import {
  longitude as startLongitude,
  latitude as startLatitude,
} from "../server/lib/start";
import { start as startSchema } from "../server/lib/validation/start";

const { data: members } = await useFetch("/api/member");

const edgeCache = reactive<{ [key: string]: { lat: number; lng: number }[] }>(
  {}
);
const currentRoutes = ref<string[][]>([]);

const currentWaypoints = computed(() =>
  currentRoutes.value.map((r) => r.map((e) => edgeCache[e] ?? []))
);

const requested = ref<string[]>([]);
const colors = ref<string[]>([]);
const iter = ref<number>(0);

const state = reactive<startSchema>({
  carsAvailable: 1,
  bikesAvailable: 4,
  bikesCapacity: 20,
});

const fetchEdge = async (a: number, b: number, type: "driving" | "cycling") => {
  const key = genKey(a, b, type);

  if (edgeCache[key] || requested.value.indexOf(key) >= 0) {
    return;
  }

  requested.value.push(key);

  const { data } = await useFetch(`/api/distance?a=${a}&b=${b}&type=${type}`);
  if (!data.value) {
    console.log(data.value);
    return [];
  }

  edgeCache[key] = data.value.geometry.map((p) => ({
    lat: p.latitude,
    lng: p.longitude,
  }));

  return data.value;
};

const start = () => {
  currentRoutes.value = [];
  let query = "";
  query += `carsAvailable=${encodeURIComponent(state.carsAvailable)}`;
  query += `&bikesAvailable=${encodeURIComponent(state.bikesAvailable)}`;
  query += `&bikesCapacity=${encodeURIComponent(state.bikesCapacity)}`;

  for (let i = 0; i <= state.carsAvailable + state.bikesAvailable; i++) {
    colors.value.push(getRandomColor());
  }

  const eventSource = new EventSource(
    `http://localhost:3000/api/start?${query}`
  );

  eventSource.onmessage = (event: MessageEvent<string>) => {
    iter.value += 1;

    if (iter.value % 10) {
      return;
    }

    const routes = JSON.parse(event.data).route;
    const newRoutes = [
      ...routes.slice(0, state.carsAvailable).map((r: any) => {
        const path = [];

        if (r[0]) {
          path.push(genKey(0, r[0], "driving"));
          fetchEdge(0, r[0], "driving");
        }

        for (let i = 0; i < r.length - 1; i++) {
          path.push(genKey(r[i], r[i + 1], "driving"));
          fetchEdge(r[i], r[i + 1], "driving");
        }

        if (r[0]) {
          path.push(genKey(r[r.length - 1], 0, "driving"));
          fetchEdge(r[r.length - 1], 0, "driving");
        }

        return path;
      }),
      ...routes.slice(state.carsAvailable).map((r: any) => {
        const path = [];

        if (r[0]) {
          path.push(genKey(0, r[0], "driving"));
          fetchEdge(0, r[0], "driving");
        }

        for (let i = 0; i < r.length - 1; i++) {
          path.push(genKey(r[i], r[i + 1], "cycling"));
          fetchEdge(r[i], r[i + 1], "cycling");
        }

        if (r[0]) {
          path.push(genKey(r[r.length - 1], 0, "driving"));
          fetchEdge(r[r.length - 1], 0, "driving");
        }

        return path;
      }),
    ];

    currentRoutes.value = newRoutes;
  };
};

const genKey = (a: number, b: number, type: "driving" | "cycling") => {
  if (a > b) {
    return `${a.toString()}|${b.toString()}|${type}`;
  } else {
    return `${b.toString()}|${a.toString()}|${type}`;
  }
};

const getRandomColor = () => {
  var letters = "0123456789ABCDEF";
  var color = "#";
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
};
</script>
