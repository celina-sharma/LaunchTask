import Account from "../models/Account.js";
import bcrypt from "bcrypt";

class AccountRepository {
  static async create(data) {
    return Account.create(data);
  }

  static async findById(id) {
    return Account.findById(id);
  }

  static async findPaginated({ status, limit = 10, cursor }) {
    const query = {status: {$ne: "deleted"}};

    if (status) {
      query.status = status;
    }

    if (cursor) {
      query.createdAt = { $lt: new Date(cursor) }};


    return Account.find(query)
      .sort({createdAt: -1 })
      .limit(limit);
  }

  static async update(id, data) {
    if(data.password){
      const salt = await bcrypt.genSalt(10);
      data.password = await bcrypt.hash(data.password,salt);
    }
    return Account.findByIdAndUpdate(id, data, { new: true,runValidators: true,    //new:true -> mongodb returns the updated document and the older one,

    });
  }

  static async delete(id) {
    return Account.findByIdAndUpdate(id,
      {status: "deleted"},
      {new: true}
    );
  }
}

export default AccountRepository;
