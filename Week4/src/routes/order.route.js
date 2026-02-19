import express from "express";
import OrderRepository from "../repositories/order.repository.js";

const router = express.Router();

// Create order
router.post("/", async (req, res) => {
  try {
    const order = await OrderRepository.create(req.body);
    res.status(201).json(order);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
});

// Get orders by account
router.get("/account/:accountId", async (req, res) => {
  try {
    const { accountId } = req.params;
    const { limit, cursor } = req.query;

    const orders = await OrderRepository.findByAccount(accountId, {
      limit: parseInt(limit) || 10,
      cursor,
    });

    res.json(orders);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
});

// Get delivered orders
router.get("/delivered", async (req, res) => {
  try {
    const orders = await OrderRepository.findDelivered();
    res.json(orders);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
});

export default router;
