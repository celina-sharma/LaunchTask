import { processJob } from "./worker.js";
import logger from "../utils/logger.js";

const jobQueue = [];

export function addJob(type, payload) {
  const job = {
    id: Date.now(),
    type,
    payload,
    attempts: 0
  };

  jobQueue.push(job);
  logger.info({ jobId: job.id, type }, "Job queued");

  processNextJob();
}

function processNextJob() {
  if (jobQueue.length === 0) return;

  const job = jobQueue.shift();
  processJob(job);
}
