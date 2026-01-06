import Product from "../models/Product.js";

class ProductRepository {
  static async create(data){
    return Product.create(data);
  }
  static async findProducts(filters) {
    const {
      search,
      minPrice,
      maxPrice,
      tags,
      sortBy = "createdAt",
      order = "desc",
      limit = 10,
      cursor,
      includeDeleted = false
    } = filters;

    const query = {};

    // Soft delete handling
    if (!includeDeleted) {
      query.deletedAt = null;
    }

    if (search) {
      query.$text = { $search: search };
    }

    if (minPrice || maxPrice) {
      query.price = {};
      if (minPrice) query.price.$gte = minPrice;
      if (maxPrice) query.price.$lte = maxPrice;
    }
    
    if (tags?.length) {
      query.tags = { $in: tags };
    }

    // Cursor pagination
    if (cursor) {
      query._id = { $lt: cursor };
    }

    return Product.find(query)
      .sort({ [sortBy]: order === "asc" ? 1 : -1 })
      .limit(limit);
  }

  static async softDelete(id) {
    return Product.findByIdAndUpdate(
      id,
      { deletedAt: new Date() },
      { new: true }
    );
  }
}

export default ProductRepository;
