import helmet from "helmet";
import cors from "cors";
import rateLimit from "express-rate-limit";

export function securityMiddleware(app) {
  app.use(
    helmet({
      contentSecurityPolicy: false, 
    })
  );

  app.use(
    cors({
      origin: "*", // later restrict to domains
      methods: ["GET", "POST", "PUT", "DELETE"],
      allowedHeaders: ["Content-Type", "Authorization"],
    })
  );

  const limiter = rateLimit({   // Rate limiting: prevent brute force
    windowMs: 60 * 1000,
    max: 5,
    message: {
      success: false,
      message: "Too many requests, please try again later",
      code: 429,
    },
  });

  app.use(limiter);
}
