
const express = require("express");
const router = express.Router();
const Screening = require("../models/Screening");
const authMiddleware = require("../middleware/authMiddleware");

router.post("/", authMiddleware, async (req, res) => {
  try {
    const { text } = req.body;

    if (typeof text !== "string" || !text.trim()) {
      return res.status(400).json({
        message: "Please enter valid text for screening.",
      });
    }

    const userId = req.user.id || req.user.userId || req.user._id;

    if (!userId) {
      return res.status(401).json({
        message: "User information missing from token.",
      });
    }

    const screening = await Screening.create({
      user: userId,
      text: text.trim(),
    });

    res.status(201).json({
      message: "Text screening response saved successfully.",
      screeningId: screening._id,
      status: screening.status,
    });
  } catch (error) {
    console.error("Screening save error:", error);

    res.status(500).json({
      message: "Unable to save the screening response.",
    });
  }
});

module.exports = router;
