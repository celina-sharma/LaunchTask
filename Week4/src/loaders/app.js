import express from "express";
import logger from "../utils/logger.js";
import { stat } from "fs";

export default function loadApp(){
    const app = express();
    app.use(express.json()); //Middleware pipeline (parses JSON body)
    app.use(express.urlencoded({extended:true})); //Middleware pipeline (parses form data)
    logger.info("Middleware loaded");

    app.get("/health",(req,res) => {
        res.status(200).json({status: "OK"});
    });
    logger.info("Routes mounted: health check");
    return app;
}