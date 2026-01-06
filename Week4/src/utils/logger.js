import pino from "pino";
import fs from "fs";
import path from "path";

const logDir = path.join(process.cwd(), "logs");

if (!fs.existsSync(logDir)) {
  fs.mkdirSync(logDir);
}

const fileStream = pino.destination({
  dest: path.join(logDir, "app.log"),
  sync: false,  
});

const logger = pino(
  { level: "info" },
  pino.multistream([
    { stream: fileStream },
    {
      stream: pino.transport({
        target: "pino-pretty",
        options: {
          colorize: true,
          translateTime: "SYS:standard",
        },
      }),
    },
  ])
);

export default logger;


