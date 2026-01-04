import ProductRepository from "../repositories/product.repository.js";
import AppError from "../utils/AppError.js";

class ProductService {
  static async getProducts(query) {
    return ProductRepository.findProducts(query);
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
