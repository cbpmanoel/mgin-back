// Read the JSON file synchronously
const fs = require('fs');

// Get the database name from the environment variable
const dbName = process.env["MONGO_DB_NAME"] || "test_db";

let data;
try {
    data = JSON.parse(fs.readFileSync('/data/init-data.json', 'utf8'));
} catch (error) {
    print('Error reading or parsing the JSON file:', error);
    quit(1); // Exit with an error code
}

// Connect to the database
print('Connecting to the database:', dbName);
db = db.getSiblingDB(dbName);

// Insert categories
if (data.categories && data.categories.length > 0) {
    try {
        db.categories.insertMany(data.categories);
        print('Categories inserted successfully.');
    } catch (error) {
        print('Error inserting categories:', error);
    }
} else {
    print('No categories to insert.');
}

// Insert items
if (data.items && data.items.length > 0) {
    try {
        db.menu_items.insertMany(data.items);
        print('Items inserted successfully.');
    } catch (error) {
        print('Error inserting items:', error);
    }
} else {
    print('No items to insert.');
}

print('Database initialization completed.');