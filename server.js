const express = require('express');
const cors = require('cors');

const app = express();
const port = 8103;

// Use the CORS middleware to allow requests from your frontend
app.use(cors({
  origin: 'https://ahaanv19.github.io', // Replace with your actual frontend URL
  credentials: true // Enable credentials
}));

// Custom middleware to set additional CORS headers
app.use((req, res, next) => {
  res.setHeader('Access-Control-Allow-Origin', 'https://ahaanv19.github.io');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  res.setHeader('Access-Control-Allow-Credentials', 'true');
  next();
});

// Define a route for the root URL
app.get('/', (req, res) => {
  res.send('Hello, World!');
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});