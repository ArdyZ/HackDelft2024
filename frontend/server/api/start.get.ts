import { start } from "../lib/validation/start";

export default defineEventHandler(async (event) => {
  const result = await getValidatedQuery(event, (body) => {
    return start.safeParse(body);
  });

  if (!result.success) {
    throw result.error.issues;
  }

  const eventStream = createEventStream(event);
  const interval = setInterval(async () => {
    await eventStream.push(`Message @ ${new Date().toLocaleTimeString()}`);
  }, 1000);

  eventStream.onClosed(async () => {
    clearInterval(interval);
    await eventStream.close();
  });

  return eventStream.send();
});
