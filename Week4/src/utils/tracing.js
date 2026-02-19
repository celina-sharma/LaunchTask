import { randomUUID } from "crypto";
import logger from "./logger.js";

export function requestTracing(req, res, next) {
  const requestId = req.headers["x-request-id"] || randomUUID();

  req.requestId = requestId;
  req.log = logger.child({ requestId });

  res.setHeader("X-Request-ID", requestId); //name and value
  next();
}