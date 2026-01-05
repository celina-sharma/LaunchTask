import AppError from "../utils/AppError.js";

export const validate =
  (schema, property = "body") =>
  (req, res, next) => {
    try {
      const parsedData = schema.parse(req[property]);
      req[property] = parsedData;
      next();
    } catch (error) {
      throw new AppError(error.issues[0].message, 400);
    }
  };
