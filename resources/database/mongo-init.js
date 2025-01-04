const fs = require('fs');

// Read the JSON file
console.log('Reading JSON file...');
const data = JSON.parse(fs.readFileSync('/data/init-data.json', 'utf8'));
console.log('JSON file read successfully.');

// Connect to MongoDB
console.log('Connecting to MongoDB...');
db = db.getSiblingDB('kiosk_db');
console.log('Connected to MongoDB.');

// Insert categories
categoriesOnData = data.categories.length;
console.log(`Inserting ${categoriesOnData} categories into categories collection...`);
db.categories.insertMany(data.categories);
console.log('Categories inserted successfully.');

// Insert items
itemsOnData = data.items.length;
console.log(`Inserting ${itemsOnData} items into menu_items collection...`);
db.menu_items.insertMany(data.items);
console.log('Items inserted successfully.');