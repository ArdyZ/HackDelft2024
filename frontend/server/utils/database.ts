import { createClient } from "../lib/db";

let db: ReturnType<typeof createClient>;

export const useDB = () => {
  if (!db) {
    db = createClient();
  }

  return db;
};
