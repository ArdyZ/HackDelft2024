export default defineEventHandler(async () => {
  const db = useDB();

  return await db.selectFrom("member").select(["id", "name"]).execute();
});
