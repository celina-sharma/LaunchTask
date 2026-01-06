import logger from "../utils/logger.js";
import { sendEmailJob } from "./email.job.js";

export async function processJob(job) {
  try {
    job.attempts += 1;

    logger.info(
      { jobId: job.id, type: job.type },
      "Job started"
    );

    if (job.type === "EMAIL_NOTIFICATION") {
      await sendEmailJob(job.payload);
    }

    logger.info(
      { jobId: job.id },
      "Job completed"
    );
  } catch (error) {
    logger.error(
      { jobId: job.id, error: error.message },
      "Job failed"
    );
  }
}
