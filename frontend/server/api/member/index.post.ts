import { create as memberCreate } from "../../lib/validation/member";

export default defineEventHandler(async (event) => {
  const result = await readValidatedBody(event, (body) =>
    memberCreate.safeParse(body)
  );

  if (!result.success) {
    throw result.error.issues;
  }

  console.log(result.data);

  const db = useDB();
  await db
    .insertInto("member")
    .values({
      name: result.data.name,
      addressName: result.data.address.name,
      addressFullname: result.data.address.fullAddress,
      addressLatitude: result.data.address.coordinates[0].toString(),
      addressLongitude: result.data.address.coordinates[1].toString(),
    })
    .executeTakeFirst();
});
