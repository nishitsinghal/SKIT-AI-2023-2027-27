
const mongoose = require("mongoose");

const screeningSchema = new mongoose.Schema(
  {
    user: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "User",
      required: false,
    },
    text: {
      type: String,
      required: true,
      trim: true,
    },
    status: {
      type: String,
      default: "received",
    },
  },
  {
    timestamps: true,
  }
);

module.exports = mongoose.model("Screening", screeningSchema);
