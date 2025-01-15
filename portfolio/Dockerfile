# Use an official Node.js image as the base
FROM node:18-slim

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install Node.js dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the port your Node.js app runs on
EXPOSE 3000

# Run the Node.js application
CMD ["node", "database_search.js"]
