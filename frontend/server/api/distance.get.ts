import { z } from "zod";
import { calculateDistance } from "../lib/mapbox/distance";

export default defineEventHandler(async (event) => {
  const query = await getValidatedQuery(event, (body) =>
    schema.safeParse(body)
  );

  if (!query.success) {
    throw query.error;
  }

  const members = await $fetch("/api/member");
  const a = members.find((member) => member.id === query.data.a);
  const b = members.find((member) => member.id === query.data.b);

  if (!a || !b) {
    throw createError("One of the members is not found.");
  }

  return await calculateDistance(a.address.coordinates, b.address.coordinates);
});

const schema = z.object({
  a: z.coerce.number().min(0),
  b: z.coerce.number().min(0),
});
