import http from "http";
const app = http.createServer((req,res) => {
    res.end("Hello from Node inside Docker");
});
app.listen(3000,() => {
    console.log("Server is running on port 3000");
});
