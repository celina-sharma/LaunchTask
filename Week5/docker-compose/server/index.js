import express from 'express';
import mongoose from 'mongoose';
import cors from 'cors';
console.log("Vivek");
const app = express();
mongoose.connect("mongodb://mongo:27017/day2db")
.then(() => console.log("Connected to MongoDB"))
.catch(err => console.log(err));

app.use(cors({
    origin:'http://localhost:3000',
    methods: 'GET,POST,PUT,PATCH,DELETE',
    allowedHeaders: 'Content-Type,Authorization',
    credentials: true
}));

app.get("/api/message", (req, res) => {
  res.json({ message: "Hello from Server" });
});


app.get('/', (req,res) => {
    res.send("Server running and connected to mongoDB");
});
 app.listen(5000,() => {
    console.log("Server running on port 5000")
 });