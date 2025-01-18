const cassandra = require('cassandra-driver');
require('dotenv').config();
const path = require('path');

// Load the secure connect bundle path and application token from environment variables
const bundlePath = path.resolve(process.env.ASTRA_DB_BUNDLE);
const authProvider = new cassandra.auth.PlainTextAuthProvider(
    'token', // 'token' is a placeholder for the application token
    process.env.ASTRA_DB_APPLICATION_TOKEN // Your Astra DB application token
);

// Create the Cassandra client using token-based authentication and the secure connect bundle
const client = new cassandra.Client({
    cloud: { secureConnectBundle: bundlePath },
    authProvider: authProvider,
    keyspace: process.env.ASTRA_KEYSPACE // Ensure keyspace is correctly set
});

// Function to connect to Astra DB
async function connect() {
    try {
        await client.connect();
        console.log('🔥 Connected to Astra DB');
    } catch (err) {
        console.log('❌ Error connecting to the DB:', err);
    }
}

// Call the connect function to initiate the connection
connect();

module.exports = client;
