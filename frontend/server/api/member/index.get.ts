export default defineEventHandler(async () => {
  const db = useDB();

  const res = await db.selectFrom("member").selectAll().execute();
  return res.map((m) => ({
    id: m.id,
    name: m.name,
    address: {
      name: m.addressName,
      fullName: m.addressFullname,
      coordinates: {
        longitude: Number(m.addressLongitude),
        latitude: Number(m.addressLatitude),
      },
    },
  }));
});
