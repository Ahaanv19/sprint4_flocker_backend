import express from 'express';
import cors from 'cors';

const app = express();
const port = process.env.PORT || 3000;

// Use the CORS middleware
app.use(cors({
  origin: ['https://nighthawkcoders.github.io', 'https://ahaanv19.github.io']
}));

// Define a route for the root URL
app.get('/', (req, res) => {
  res.send('Hello, World!');
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});