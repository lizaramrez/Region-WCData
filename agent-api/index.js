import express from 'express';
import fs from 'fs';
import csv from 'csv-parser';

const app = express();
const PORT = 3001;

// Helper to read CSV and return data as array of objects
function readCSV(filePath) {
  return new Promise((resolve, reject) => {
    const results = [];
    fs.createReadStream(filePath)
      .pipe(csv())
      .on('data', (data) => results.push(data))
      .on('end', () => resolve(results))
      .on('error', reject);
  });
}

// Endpoint: Get latest update date for a service
app.get('/api/latest-update', async (req, res) => {
  const { service, source = 'OPG' } = req.query;
  const file = source === 'IC3' ? '../IC3RegionData.csv' : '../OPGRegionData.csv';
  try {
    const data = await readCSV(new URL(file, import.meta.url));
    const found = data.find(row => (row['Service Name'] || '').toLowerCase() === (service || '').toLowerCase());
    if (found && found['LastUpdate']) {
      res.json({ service, lastUpdate: found['LastUpdate'] });
    } else {
      res.status(404).json({ error: 'Service or update date not found.' });
    }
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Endpoint: Ping service owner (mock)
app.post('/api/ping-owner', express.json(), async (req, res) => {
  const { service, source = 'OPG' } = req.body;
  const file = source === 'IC3' ? '../IC3RegionData.csv' : '../OPGRegionData.csv';
  try {
    const data = await readCSV(new URL(file, import.meta.url));
    const found = data.find(row => (row['Service Name'] || '').toLowerCase() === (service || '').toLowerCase());
    if (found && found['ServiceOwner']) {
      // Here you would call Microsoft Graph API or Bot to send a Teams message
      // For now, just mock the response
      res.json({ service, owner: found['ServiceOwner'], message: `Ping sent to ${found['ServiceOwner']}` });
    } else {
      res.status(404).json({ error: 'Service or owner not found.' });
    }
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(PORT, () => {
  console.log(`Agent API server running on http://localhost:${PORT}`);
});
