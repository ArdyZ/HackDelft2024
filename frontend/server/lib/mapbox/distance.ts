export const calculateDistance = defineCachedFunction(
  async (
    a: { longitude: number; latitude: number },
    b: { longitude: number; latitude: number },
    type: "driving" | "cycling"
  ) => {
    const config = useRuntimeConfig();
    const encodedToken = encodeURIComponent(config.mapboxKey);
    const encodedPath = encodeURIComponent(
      `${a.longitude},${a.latitude};${b.longitude},${b.latitude}`
    );

    const res = await $fetch<{
      routes: {
        weight: number;
        duration: number;
        distance: number;
        geometry: {
          coordinates: [number, number][];
        };
      }[];
    }>(
      `https://api.mapbox.com/directions/v5/mapbox/${type}/${encodedPath}?access_token=${encodedToken}&geometries=geojson&overview=full&steps=false&notifications=none`
    );

    const r = res.routes[0];
    if (!r) {
      throw createError("No route found");
    }

    return {
      weight: r.weight,
      distance: r.distance,
      duration: r.duration,
      geometry: r.geometry.coordinates.map((c) => ({
        longitude: c[0],
        latitude: c[1],
      })),
    };
  },
  {
    maxAge: 4 * 60 * 60,
    name: "calc_distance",
    getKey: (
      a: { longitude: number; latitude: number },
      b: { longitude: number; latitude: number }
    ) => {
      if (a.latitude + a.longitude >= b.latitude + b.longitude) {
        return `${a.longitude},${a.latitude};${b.longitude},${b.latitude}`;
      } else {
        return `${b.longitude},${b.latitude};${a.longitude},${a.latitude}`;
      }
    },
  }
);
