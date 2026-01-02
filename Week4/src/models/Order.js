import mongoose, { mongo } from "mongoose";

const orderSchema = new mongoose.Schema(
  {
    accountId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "Account",
      required: true,
      index: true,
    },

    amount: {
      type: Number,
      required: true,
      min: 0,
    },

    status: {
      type: String,
      enum: ["pending", "completed", "cancelled"],
      default: "pending",
      index: true,
    },

    deliveredAt: {
      type: Date,
    },
  },
  {
    timestamps: true,
  }
);
  
orderSchema.index({ accountId: 1, createdAt: -1 });  // Compound index for read-heavy queries
orderSchema.index({ deliveredAt: 1 }, { sparse: true });  // Sparse index (only orders that are delivered)
orderSchema.index(
  { createdAt: 1 },
  { expireAfterSeconds: 60 * 60 * 24 * 90 }  // TTL index (auto-delete after 90 days)
);

const Order = mongoose.model("Order",orderSchema);
export default Order;