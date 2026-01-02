import Account from "../models/Account.js";

class AccountRepository {
  static async create(data) {
    return Account.create(data);
  }

  static async findById(id) {
    return Account.findById(id);
  }

  static async findPaginated({ status, limit = 10, cursor }) {
    const query = {};

    if (status) {
      query.status = status;
    }

    if (cursor) {
      query._id = { $lt: cursor };
    }

    return Account.find(query)
      .sort({ _id: -1 })
      .limit(limit);
  }

  static async update(id, data) {
    return Account.findByIdAndUpdate(id, data, { new: true });
  }

  static async delete(id) {
    return Account.findByIdAndDelete(id);
  }
}

export default AccountRepository;
