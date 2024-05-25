import { create as memberCreate } from "../../lib/validation/member";

export default defineEventHandler(async (event) => {
  const result = await readValidatedBody(event, (body) =>
    memberCreate.safeParse(body)
  );

  if (!result.success) {
    throw result.error.issues;
  }

  const db = useDB();
  await db.insertInto("member").values(result.data).executeTakeFirst();
});
