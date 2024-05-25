import { SqliteDialect } from "kysely";
import { defineConfig } from "kysely-ctl";

import SQLite from "better-sqlite3";

export default defineConfig({
  dialect: new SqliteDialect({
    database: new SQLite("database.db"),
  }),
  migrations: {
    migrationFolder: "./server/lib/db/migrations",
  },
  seeds: {
    seedFolder: "./server/lib/db/seeds",
  },
});
