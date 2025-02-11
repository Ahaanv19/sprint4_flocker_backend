const express = require('express');
const cors = require('cors');

const app = express();
const port = 8103;

// Use the CORS middleware to allow requests from your frontend
app.use(cors({
  origin: 'https://ahaanv19.github.io', // Specify the exact origin of your frontend
  credentials: true // Enable credentials
}));

// Define a route for the root URL
app.get('/', (req, res) => {
  res.send('Hello, World!');
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});