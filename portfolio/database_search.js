
const express = require('express');
const cors = require('cors');
const app = express();
const port = 3000;

const { MongoClient } = require('mongodb');
//const uri = 'mongodb://localhost:27017';
const uri = 'mongodb://mongo-db:27017';

const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });

app.use(cors());

app.get('/search', async (req, res) => {
  const symbol = req.query.query.toUpperCase();

  try {
    console.log(`Connecting to MongoDB...`);
    await client.connect();
    console.log(`Connected to MongoDB`);

    const database = client.db('admin');
    const collections = await database.listCollections().toArray();

    const assetData = [];

    for (const collection of collections) {
      const collectionName = collection.name;

      // Exclude 'system.version' collection
      if (collectionName === 'system.version') {
        console.log(`Skipping collection: ${collectionName}`);
        continue;
      }

      console.log(`Using collection: ${collectionName}`);

      const collectionData = await database.collection(collectionName).find({}).toArray();
      console.log(`Raw data for ${collectionName}:`, collectionData);

      assetData.push(
        ...collectionData.map(document => ({
          ...document[symbol],
          collection: collectionName,
        }))
      );
    }

    console.log(`Extracted asset data:`, assetData);

    res.json(assetData);
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
