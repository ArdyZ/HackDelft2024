import { z } from "zod";

export const create = z.object({
  name: z.string().min(3).max(30),
});
export type create = z.infer<typeof create>;
