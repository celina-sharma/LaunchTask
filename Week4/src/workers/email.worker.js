import { Worker } from "bullmq";
import { connection } from "../utils/redis.js";
import logger from "../utils/logger.js";
import { sendEmailJob } from "../jobs/email.job.js";

console.log("EMAIL WORKER STARTED AND LISTENING");

const worker = new Worker(
  "email-queue",
  async (job) => {
    const { requestId, email } = job.data;

    logger.info(
      {
        jobId: job.id,
        requestId,
        attempt: job.attemptsMade,
        email,
      },
      "Worker picked email job"
    );

    await sendEmailJob(job.data);

    logger.info(
      {
        jobId: job.id,
        requestId,
        email,
      },
      "Worker completed email job"
    );
  },
  { connection }
);

// When job fails (retry/backoff will trigger automatically)
worker.on("failed", (job, err) => {
  logger.error(
    {
      jobId: job.id,
      requestId: job.data?.requestId,
      error: err.message,
    },
    "Email job failed"
  );
});

// When job succeeds
worker.on("completed", (job) => {
  logger.info(
    {
      jobId: job.id,
      requestId: job.data?.requestId,
    },
    "Email job processed successfully"
  );
});

export default worker;
