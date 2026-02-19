import ProductService from "../services/product.service.js";
import { enqueueEmailJob } from "../jobs/email.job.js";
export const createProduct = async (req, res, next) => {
  try {
    const product = await ProductService.createProduct(req.body);
    await enqueueEmailJob(
      {
        email: "test@example.com",
        productName:product.name,
        requestId: req.requestId
      }
    )
    res.status(201).json({
      success: true,
      data: product,
    });
  } catch (err) {
    next(err);
  }
};

export const getProducts = async (req, res, next) => {
  try {
    const products = await ProductService.getProducts({
      ...req.query,
      tags: req.query.tags?.split(","),
    });

    res.json({
      success: true,
      data: products,
    });
  } catch (err) {
    next(err);
  }
};

export const deleteProduct = async (req, res, next) => {
  try {
    await ProductService.deleteProduct(req.params.id);
    res.json({
      success: true,
      message: "Product deleted",
    });
  } catch (err) {
    next(err);
  }
};

export default { createProduct, getProducts, deleteProduct };
