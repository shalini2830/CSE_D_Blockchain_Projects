#!/bin/bash
# Start Ganache with persistent database
# This ensures votes persist between restarts

echo "🚀 Starting Ganache with persistent storage..."
echo "📁 Database location: ./ganache-db"
echo "💾 All votes and contracts will be saved to disk"
echo ""

# Create database directory if it doesn't exist
mkdir -p ganache-db

# Start Ganache with database persistence
ganache-cli --db ganache-db --deterministic