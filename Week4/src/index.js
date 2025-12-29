import config from "./config/index.js";
import logger from "./utils/logger.js";
import loadDB from "./loaders/db.js";
import loadApp from "./loaders/app.js";


async function startServer() {
    try {
        await loadDB();
        const app = loadApp();
        const server = app.listen(config.port,() => {
            logger.info(`Server started on this port ${config.port}`);
        });
        process.on("SIGINT",async() => {
            logger.info("Server shutting down");
            server.close(() => {
                process.exit(0);
            });
        });
    } catch (error) {
       logger.info("Startup failed",error);
       process.exit(1); 
    }
}
startServer();