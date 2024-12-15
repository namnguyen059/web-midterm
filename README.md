# MongoDB Setup and Sharding Configuration Guide  

This repository provides a structured guide for setting up **MongoDB 7.0**, managing sharded clusters, and executing essential database operations. Follow the step-by-step instructions to configure MongoDB on a local environment.

---

## **Table of Contents**  
1. [Prerequisites](#1-prerequisites)  
2. [Installation and Configuration](#2-installation-and-configuration)  
3. [Starting and Stopping MongoDB Services](#3-starting-and-stopping-mongodb-services)  
4. [Replica Sets and Sharding Setup](#4-replica-sets-and-sharding-setup)  
5. [Sharding Configuration](#5-sharding-configuration)  
6. [Essential MongoDB Operations](#6-essential-mongodb-operations)  

---

## **1. Prerequisites**  
Ensure the following tools are installed:  
- **Homebrew** (for macOS users)  
- **MongoDB Community Edition 7.0**  

---

## **2. Installation and Configuration**  

### **Step 1: Install MongoDB 7.0**  
```bash
brew tap mongodb/brew  
brew install mongodb-community@7.0  
```

### **Step 2: Create Data Directories and Logs**  
Prepare directories for replica sets and configuration servers:  
```bash
mkdir -p data/rs0 data/rs1 data/rs2 data/rs3 data/rs4 data/rs5  
mkdir -p data/cfg0 data/cfg1 data/cfg2  
mkdir -p logs  
```

---

## **3. Starting and Stopping MongoDB Services**  

### **Start MongoDB Services**  
```bash
brew services start mongodb-community@7.0  
```

### **Stop MongoDB Services**  
```bash
brew services stop mongodb-community@7.0  
```

### **List Running Services**  
```bash
brew services list  
```

### **Check Running MongoDB Process**  
```bash
ps aux | grep mongod  
```

### **Kill MongoDB Processes**  
```bash
kill $(ps aux | grep '[m]ongod --config' | awk '{print $2}')  
pkill -f mongos  
```

### **Verify MongoDB Port**  
```bash
lsof -i :27017  
```

---

## **4. Replica Sets and Sharding Setup**  

### **Step 1: Config Server Replica Set**  
Start a MongoDB shell and initialize the configuration server replica set:  
```bash
mongosh --port 27020
rs.initiate({
  _id: "configReplSet",
  configsvr: true,
  members: [
    { _id: 0, host: "localhost:27020" },
    { _id: 1, host: "localhost:27021" },
    { _id: 2, host: "localhost:27022" }
  ]
})
```

### **Step 2: Shard Replica Sets**  
1. **Initialize Shard 1**  
   ```bash
   mongosh --port 27017
   rs.initiate({
     _id: "shard_1",
     members: [
       { _id: 0, host: "localhost:27017" },
       { _id: 1, host: "localhost:27018" },
       { _id: 2, host: "localhost:27019" }
     ]
   })
   ```

2. **Initialize Shard 2**  
   ```bash
   mongosh --port 27023
   rs.initiate({
     _id: "shard_2",
     members: [
       { _id: 0, host: "localhost:27023" },
       { _id: 1, host: "localhost:27024" },
       { _id: 2, host: "localhost:27025" }
     ]
   })
   ```

3. **Check Replica Set Status**  
   ```bash
   rs.conf()
   rs.status()
   ```

### **Step 3: Start mongos Process**  
Ensure `mongos.conf` is properly configured and run:  
```bash
mongos --config mongos.conf  
```

---

## **5. Sharding Configuration**  

### **Connect to mongos**  
```bash
mongosh --port 27026  
```

### **Add Shards to Cluster**  
```bash
sh.addShard("shard_1/localhost:27017,localhost:27018,localhost:27019")  
sh.addShard("shard_2/localhost:27023,localhost:27024,localhost:27025")  
```

### **Enable Sharding for a Database**  
```bash
use ecommerce  
sh.enableSharding("ecommerce")  
```

### **Shard Collections**  
Shard collections using a specified key:  
```bash
sh.shardCollection("ecommerce.products", { product_id: 1 })  
sh.shardCollection("ecommerce.users", { user_id: 1 })  
```

### **View Sharding Status**  
```bash
sh.status()  
```

---

## **6. Essential MongoDB Operations**  

### **Database and Collection Operations**  
1. **List Databases**  
   ```bash
   show dbs  
   ```

2. **Use a Specific Database**  
   ```bash
   use ecommerce  
   ```

3. **List Collections**  
   ```bash
   show collections  
   ```

4. **View Collection Documents**  
   ```bash
   db.products.find()  
   db.users.find()  
   ```

5. **Count Documents**  
   ```bash
   db.products.countDocuments()  
   db.users.countDocuments()  
   ```

6. **Delete Documents**  
   ```bash
   db.products.deleteMany({})  
   db.users.deleteMany({})  
   ```

7. **Drop Collections and Database**  
   ```bash
   db.products.drop()  
   db.dropDatabase()  
   ```

### **Index Operations**  
1. **Create Indexes**  
   ```bash
   db.products.createIndex({ product_id: 1 })  
   db.users.createIndex({ user_id: 1 })  
   ```

2. **View Indexes**  
   ```bash
   db.products.getIndexes()  
   db.users.getIndexes()  
   ```

3. **Drop Indexes**  
   ```bash
   db.products.dropIndex("product_id_1")  
   db.users.dropIndex("user_id_1")  
   ```

---

## **Scripts and Automation**  
1. **Executable Shell Script**  
   Ensure the script is executable:  
   ```bash
   chmod +x start_mongodb.sh  
   ./start_mongodb.sh  
   ```

2. **Script Contents**  
   A sample script can include starting services, setting ports, and initiating configurations.

---

## **Additional Notes**  
- Ports used in this setup: `27017`, `27018`, `27019`, `27020`, `27021`, `27022`, `27023`, `27024`, `27025`, `27026`.  
- Always verify active connections with `lsof -i :<port>` before starting services.  

