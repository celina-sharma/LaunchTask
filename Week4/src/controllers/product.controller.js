import ProductService from "../services/product.service.js";

export const getProducts = async (req, res, next) => {
  try {
    const products = await ProductService.getProducts({
      ...req.query,
      tags: req.query.tags?.split(",")
    });

    res.json({
      success: true,
      data: products
    });
  } catch (err) {
    next(err);
  }
};

export const deleteProduct = async (req, res, next) => {
  try {
    const product = await ProductService.deleteProduct(req.params.id);

    res.json({
      success: true,
      message: "Product deleted"
    });
  } catch (err) {
    next(err);
  }
};
