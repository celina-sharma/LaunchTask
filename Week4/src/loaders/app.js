import express from "express";
import logger from "../utils/logger.js";
import productRoutes from "../routes/product.route.js";
import accountRoutes from "../routes/account.route.js"
import orderRoutes from "../routes/order.route.js"
import { errorHandler } from "../middlewares/error.middleware.js";
import { securityMiddleware } from "../middlewares/security.js";
import { requestTracing } from "../utils/tracing.js";

export default function loadApp() {
  const app = express();

  app.use(express.json({ limit: "10kb" }));
  app.use(express.urlencoded({ extended: true, limit: "10kb" }));
  logger.info("Base middleware loaded");

  app.use(requestTracing);
  logger.info("Request tracing enabled");

  securityMiddleware(app);
  logger.info("Security middleware loaded");

  app.get("/health", (req, res) => {
    res.status(200).json({ status: "OK" });
  });
  logger.info("Routes mounted: health check"
);

  app.use("/accounts", accountRoutes);
  logger.info("Routes mounted: accounts");

  app.use("/orders",orderRoutes);
  logger.info("Routes mounted: orders");

  app.use("/products", productRoutes);
  logger.info("Routes mounted: products");

  app.use(errorHandler);
  return app;
}
