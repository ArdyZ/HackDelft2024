import { z } from "zod";

export const create = z.object({
  name: z.string().min(3).max(30),
  address: z.object({
    name: z.string().min(3).max(120),
    fullAddress: z.string().min(3).max(120),
    coordinates: z.tuple([z.number(), z.number()]),
  }),
});
export type create = z.infer<typeof create>;
