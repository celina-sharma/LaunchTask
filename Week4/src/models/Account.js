import mongoose from "mongoose";
import bcrypt from "bcrypt";

const accountSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: true,
      trim: true,
      minlength: 2,
    },
    email: {
      type: String,
      required: true,
      trim: true,
      unique: true,   //no duplicates in email field
      lowercase: true,
      match: [/^\S+@\S+\.\S+$/, "Invalid email format"],
    },
    password: {
      type: String,
      required: true,
      minlength: 6,
      select: false,
    },
    status: {
      type: String,
      enum: ["active", "blocked","deleted"],
      default: "active",
    },
  },
  {
    timestamps: true,  //automatically added createdAt and updatedAt 
  }
);
accountSchema.pre("save", async function () {
  if (!this.isModified("password")) return;   //prevents double hashing

  const salt = await bcrypt.genSalt(10);
  this.password = await bcrypt.hash(this.password, salt);
});
 //pre-save hook(password hashing)

accountSchema.virtual("accountAge").get(function () {
  return Math.floor(
    (Date.now() - this.createdAt.getTime()) / (1000 * 60 * 60 * 24)  //returning number of days since account creation
  );
});



accountSchema.index({ status: 1, createdAt: -1 });

const Account = mongoose.model("Account", accountSchema);
export default Account;
