import type { Kysely } from "kysely";
import { fakerNL as faker } from "@faker-js/faker";

export async function seed(db: Kysely<any>): Promise<void> {
  for (let i = 0; i < 25; i++) {
    await db
      .insertInto("member")
      .values({
        name: `${faker.person.firstName()} ${faker.person.lastName()}`,
      })
      .executeTakeFirst();
  }
}
