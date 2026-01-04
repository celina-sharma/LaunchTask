import Product from "../models/Product.js";

class ProductRepository {
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

    // Text search
    if (search) {
      query.$text = { $search: search };
    }

    // Price range
    if (minPrice || maxPrice) {
      query.price = {};
      if (minPrice) query.price.$gte = minPrice;
      if (maxPrice) query.price.$lte = maxPrice;
    }

    // Tags OR condition
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
