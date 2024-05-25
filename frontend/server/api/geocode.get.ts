import { z } from "zod";

import { lookup } from "../lib/mapbox/geocode";

export default defineEventHandler(async (event) => {
  const query = await getValidatedQuery(event, (body) =>
    schema.safeParse(body)
  );

  if (!query.success) {
    throw query.error;
  }

  return await lookup(query.data.q);
});

const schema = z.object({
  q: z.string().min(1).max(200),
});
