export const lookup = defineCachedFunction(
  async (address: string) => {
    const config = useRuntimeConfig();
    const encodedToken = encodeURIComponent(config.mapboxKey);
    const encodedAddress = encodeURIComponent(address);

    const res = await $fetch<{
      features: {
        type: "Feature";
        id: string;
        geometry: {
          type: "Point";
          coordinates: [number, number];
        };
        properties: {
          mapbox_id: string;
          feature_type: "street";
          full_address: string;
          name: string;
          name_preferred: string;
          coordinates: { longitude: number; latitude: number };
          place_formatted: string;
          context: object;
        };
      }[];
    }>(
      `https://api.mapbox.com/search/geocode/v6/forward?access_token=${encodedToken}&q=${encodedAddress}&proximity=ip&country=NL`
    );

    return res.features.map((feature) => ({
      name: feature.properties.name_preferred,
      fullAddress: feature.properties.full_address,
      coordinates: feature.geometry.coordinates,
    }));
  },
  {
    maxAge: 4 * 60 * 60,
    name: "geocode_lookup",
    getKey: (address: string) => address,
  }
);
