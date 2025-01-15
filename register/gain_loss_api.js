const express = require('express');
const cors = require('cors');
const app = express();
const port = 3000;

const { MongoClient } = require('mongodb');
const uri = 'mongodb://localhost:27017';
const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });

app.use(cors());

app.get('/closing-price', async (req, res) => {
  const symbol = req.query.symbol.toUpperCase();
  const startDate = new Date(req.query.startDate);
  const endDate = new Date(req.query.endDate);

  try {
    console.log(`Connecting to MongoDB...`);
    await client.connect();
    console.log(`Connected to MongoDB`);

    const database = client.db('admin');
    const collections = await database.listCollections().toArray();

    const closingPrices = [];

    for (const collection of collections) {
      const collectionName = collection.name;

      const query = {
        symbol: symbol,
        timestamp: { $gte: startDate, $lte: endDate }
      };

      const collectionData = await database.collection(collectionName).find(query).toArray();

      if (collectionData.length > 0) {
        const latestClosingPrice = collectionData[0].closingPrice;
        closingPrices.push({ collection: collectionName, latestClosingPrice });
      }
    }

    if (closingPrices.length === 0) {
      return res.status(404).json({ message: 'No data found for the specified symbol and date range' });
    }

    res.json({ symbol: symbol, closingPrices: closingPrices });
  } catch (err) {
    console.error(`Error:`, err);
    res.status(500).send('Internal Server Error');
  } finally {
    console.log(`Closing MongoDB connection...`);
    await client.close();
    console.log(`MongoDB connection closed`);
  }
});

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});
