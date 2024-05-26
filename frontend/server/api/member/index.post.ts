import { create as memberCreate } from "../../lib/validation/member";

export default defineEventHandler(async (event) => {
  const result = await readValidatedBody(event, (body) =>
    memberCreate.safeParse(body)
  );

  if (!result.success) {
    throw result.error.issues;
  }

  const db = useDB();
  await db
    .insertInto("member")
    .values({
      name: result.data.name,
      addressName: result.data.address.name,
      addressFullname: result.data.address.fullAddress,
      addressLatitude: result.data.address.coordinates.latitude.toString(),
      addressLongitude: result.data.address.coordinates.longitude.toString(),
    })
    .executeTakeFirst();
});
