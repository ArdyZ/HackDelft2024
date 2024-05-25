import type { Kysely } from "kysely";
import { fakerNL as faker } from "@faker-js/faker";

export async function seed(db: Kysely<any>): Promise<void> {
  for (let i = 0; i < 25; i++) {
    const coordinates = faker.location.nearbyGPSCoordinate({
      origin: [51.998752, 4.373719],
    });
    const address = faker.location.streetAddress();

    await db
      .insertInto("member")
      .values({
        name: `${faker.person.firstName()} ${faker.person.lastName()}`,
        addressName: address,
        addressFullname: address,
        addressLatitude: coordinates[0].toString(),
        addressLongitude: coordinates[1].toString(),
      })
      .executeTakeFirst();
  }
}
