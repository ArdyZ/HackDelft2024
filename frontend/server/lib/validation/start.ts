import { z } from "zod";

export const start = z.object({
  carsAvailable: z.coerce.number().min(1),
  bikesAvailable: z.coerce.number().min(1),
  bikesCapacity: z.coerce.number().min(5),
});
export type start = z.infer<typeof start>;
