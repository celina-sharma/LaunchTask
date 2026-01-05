import express from "express"
import { getProducts,deleteProduct } from "../controllers/product.controller.js"
import { validate } from "../middlewares/validate.js";
import { createProductSchema } from "../validators/product.schema.js";
import * as productController from "../controllers/product.controller.js"

const router = express.Router();

router.get("/",getProducts)
router.delete("/:id",deleteProduct)
router.post(
  "/",
  validate(createProductSchema),
  productController.createProduct
);


export default router;