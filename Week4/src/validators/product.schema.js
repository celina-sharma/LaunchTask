import { z } from "zod";

export const createProductSchema = z.object({
  name: z
    .string()
    .min(3, "Name must be at least 3 characters")
    .max(100, "Name must be less than 100 characters"),

  price: z
    .number()
    .positive("Price must be a positive number"),

  tags: z
    .array(z.string().min(2))
    .max(10)
    .optional(),
});
