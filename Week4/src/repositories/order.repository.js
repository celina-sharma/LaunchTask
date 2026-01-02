import Order from "../models/Order.js";

class OrderRepository {
  static async create(data) {
    return Order.create(data);
  }

  static async findByAccount(accountId, { limit = 10, cursor }) {
    const query = { accountId };

    if (cursor) {
      query._id = { $lt: cursor };
    }

    return Order.find(query)
      .sort({ _id: -1 })
      .limit(limit);
  }

  static async findDelivered() {
    return Order.find({ deliveredAt: { $exists: true } });
  }
}

export default OrderRepository;
