import Order from "../models/Order.js";
import mongoose from "mongoose";

class OrderRepository {
  static async create(data) {
    return Order.create(data);
  }

  static async findByAccount(accountId, { limit = 10, cursor }) {
    const query = { accountId };

    if (cursor) {
      query._id = { $lt: new mongoose.Types.ObjectId(cursor) };
    }

    return Order.find(query)
      .sort({ _id: -1 })
      .limit(limit)
      .populate("accountId","name email") //populate user
      .populate("products.productId", "name price"); //populate products
  }

  static async findDelivered() {
    return Order.find({ deliveredAt: { $exists: true } });
  }
}

export default OrderRepository;
