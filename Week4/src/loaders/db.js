import mongoose from "mongoose";
import logger from "../utils/logger.js";
import config from "../config/index.js";

export default async function loadDB(){
  try {
    // console.log("DB URL:", config.dbUrl);
    await mongoose.connect(config.dbUrl);
    logger.info("Database connected")
  } catch (error) {
    logger.error("Database connection fails",error);
    process.exit(1);
  }
}
