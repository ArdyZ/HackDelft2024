import { spawn } from "child_process";

import { start } from "../lib/validation/start";

export default defineEventHandler(async (event) => {
  const result = await getValidatedQuery(event, (body) => {
    return start.safeParse(body);
  });

  if (!result.success) {
    throw result.error.issues;
  }

  const eventStream = createEventStream(event);

  const algo = spawn("python3", [
    "../algorithm/genetic.py",
    result.data.carsAvailable.toString(),
    result.data.bikesAvailable.toString(),
    result.data.bikesCapacity.toString(),
  ]);

  algo.stdout.on("data", (buf) => {
    const data = JSON.parse(buf.toString());
    eventStream.push(JSON.stringify(data));
  });

  algo.stderr.on("data", (data) => {
    console.error(`Err: ${data}`);
  });

  algo.on("close", () => {
    console.info("Algorithm done.");
    eventStream.close();
  });

  eventStream.onClosed(async () => {
    await eventStream.close();
    algo.kill();
    console.info("Evenstream closed.");
  });

  return eventStream.send();
});
