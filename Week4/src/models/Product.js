import mongoose from "mongoose";

const productSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: true,
      trim: true
    },

    price: {
      type: Number,
      required: true,
      min: 0
    },

    tags: {
      type: [String],
      index: true
    },

    deletedAt: {
      type: Date,
      default: null
    }
  },
  { timestamps: true }
);

productSchema.index({ price: 1 });
productSchema.index({ name: "text" });

const Product = mongoose.model("Product", productSchema);
export default Product;
