import logger from "../utils/logger.js";
import { emailQueue } from "../queues/email.queue.js";

export async function sendEmailJob(payload) {
  logger.info(
    { email: payload.email },
    "Email job started"
  );

  await new Promise((resolve) => setTimeout(resolve, 2000));

  logger.info(
    { email: payload.email },
    "Email sent successfully"
  );
  console.log("EMAIL SENT TO:",payload.email);
}

export async function enqueueEmailJob(data , requestId) {
  await emailQueue.add(
    "send-email",   // job name
    data,           // payload
    {
      attempts: 3,
      backoff: {
        type: "exponential", //next delays increase: 3s,6s,12s
        delay: 3000
      }
    }
  );
}
