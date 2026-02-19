import dotenv from "dotenv";
import path from "path";

const env = process.env.NODE_ENV || "local";

const envFile = `.env.${env}`;
dotenv.config({
    path: path.resolve(process.cwd(),envFile),
});

export default({
    env,
    port: process.env.PORT,
    dbUrl: process.env.MONGO_URI,
})