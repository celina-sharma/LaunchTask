import ProductRepository from "../repositories/product.repository.js";
import logger from "../utils/logger.js";
import AppError from "../utils/AppError.js";

class ProductService {
  static async getProducts(filters) {
    logger.info("User addition started :");
    return ProductRepository.findProducts(filters);
  }

  static async createProduct(data) {
    return ProductRepository.create(data);
  }

  static async deleteProduct(id) {
    const product = await ProductRepository.softDelete(id);
    if (!product) {
      throw new AppError("Product not found", 404);
    }
    return product;
  }
}

export default ProductService;
