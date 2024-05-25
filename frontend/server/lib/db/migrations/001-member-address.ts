import { Kysely } from "kysely";

export async function up(db: Kysely<any>): Promise<void> {
  await db.schema
    .alterTable("member")
    .addColumn("addressName", "varchar(120)", (col) => col.notNull())
    .execute();

  await db.schema
    .alterTable("member")
    .addColumn("addressFullname", "varchar(120)", (col) => col.notNull())
    .execute();

  await db.schema
    .alterTable("member")
    .addColumn("addressLongitude", "varchar(25)", (col) => col.notNull())
    .execute();

  await db.schema
    .alterTable("member")
    .addColumn("addressLatitude", "varchar(25)", (col) => col.notNull())
    .execute();
}

export async function down(db: Kysely<any>): Promise<void> {
  await db.schema
    .alterTable("member")
    .dropColumn("addressName")
    .dropColumn("addressFullname")
    .dropColumn("addressLongitude")
    .dropColumn("addressLatitude")
    .execute();
}
