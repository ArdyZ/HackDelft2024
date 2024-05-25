import SQLite from "better-sqlite3";
import { Kysely, SqliteDialect } from "kysely";

import { MemberTable } from "./types/member";

export * from "./types/member";

export interface Database {
  member: MemberTable;
}

export const createClient = () => {
  const dialect = new SqliteDialect({
    database: new SQLite("database.db"),
  });

  return new Kysely<Database>({
    dialect,
  });
};
