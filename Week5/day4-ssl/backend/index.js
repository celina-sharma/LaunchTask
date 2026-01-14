import express from "express";

const app = express();

app.get("/api", (req, res) => {
  res.json({
    message: "Secure API response",
    container: process.env.HOSTNAME
  });
});

app.listen(3000, () => {
  console.log("Backend running on port 3000");
});
