import { z } from "zod";
import { calculateDistance } from "../lib/mapbox/distance";
import {latitude, longitude} from "~/server/lib/start";

export default defineEventHandler(async (event) => {
  const query = await getValidatedQuery(event, (body) =>
    schema.safeParse(body)
  );

  if (!query.success) {
    throw query.error;
  }

  const members = await $fetch("/api/member");
  const b = members.find((member) => member.id === query.data.b);
  const type = query.data.type;

  if (!b) {
    throw createError("One of the members is not found.");
  }

  const ewi: { longitude: number; latitude: number } = { longitude: longitude, latitude: latitude}

  return await calculateDistance(ewi, b.address.coordinates, type);
});

const schema = z.object({
  b: z.coerce.number().min(0),
  type: z.enum(["driving", "cycling"])
});
