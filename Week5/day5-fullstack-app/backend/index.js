import express from 'express';
import mongoose from 'mongoose';

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 5000;
const MONGO_URI = process.env.MONGO_URI;

mongoose.connect(MONGO_URI)
  .then(() => console.log("Connected to MongoDB"))
  .catch(err => console.error("MongoDB connection error:", err));

const Message = mongoose.model('Message', { text: String, date: { type: Date, default: Date.now } });

app.get('/api/messages', async (req, res) => {
  const messages = await Message.find().sort({ date: -1 });
  res.json(messages);
});

app.post('/api/messages', async (req, res) => {
  const newMessage = new Message({ text: req.body.text });
  await newMessage.save();
  res.status(201).json(newMessage);
});

app.get('/api/health', (req, res) => res.status(200).send("Healthy"));
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));