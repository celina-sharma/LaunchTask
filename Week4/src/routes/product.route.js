import express from "express";
import { validate } from "../middlewares/validate.js";
import { createProductSchema } from "../validators/product.schema.js";
import * as productController from "../controllers/product.controller.js";
import { enqueueEmailJob } from "../jobs/email.job.js";
const router = express.Router();

router.get("/", productController.getProducts);
router.delete("/:id", productController.deleteProduct);
router.post(
  "/",
  validate(createProductSchema),
  productController.createProduct
);

router.post("/notify", async (req, res) => {
  req.log.info("Notify API called");

  await enqueueEmailJob({
    email: "user123@example.com",
    requestId: req.requestId
  });

  req.log.info("Email job enqueued");

  res.status(202).json({
    success: true,
    message: "Job accepted & running in background",
    requestId: req.requestId
  });
});

export default router;
