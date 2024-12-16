import express from 'express';

const app = express();
const port = process.env.PORT || 8887;

// Custom middleware to set CORS headers
app.use((req, res, next) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.header(
    'Access-Control-Allow-Headers', 'Content-Type, Accept');
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