import express from "express";
import AccountRepository from "../repositories/account.repository.js";

const router = express.Router();

// Create account
router.post("/", async (req, res) => {
  try {
    const account = await AccountRepository.create(req.body);
    res.status(201).json(account);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
});

// Get single account
router.get("/:id", async (req, res) => {
  try {
    const account = await AccountRepository.findById(req.params.id);

    if (!account) {
      return res.status(404).json({ message: "Account not found" });
    }

    res.json(account);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
});

// Get paginated accounts
router.get("/", async (req, res) => {
  try {
    const { status, limit, cursor } = req.query;

    const accounts = await AccountRepository.findPaginated({
      status,
      limit: parseInt(limit) || 10,
      cursor,
    });

    res.json(accounts);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
});

// Update account
router.patch("/:id", async (req, res) => {
  try {
    const account = await AccountRepository.update(req.params.id, req.body);

    if (!account) {
      return res.status(404).json({ message: "Account not found" });
    }

    res.json(account);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
});

// Delete account
router.delete("/:id", async (req, res) => {
  try {
    const account = await AccountRepository.delete(req.params.id);

    if (!account) {
      return res.status(404).json({ message: "Account not found" });
    }

    res.json({ message: "Account deleted successfully" });
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
});

export default router;
