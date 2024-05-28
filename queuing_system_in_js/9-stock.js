const express = require('express');
const redis = require('redis');
const { promisify } = require('util');

const app = express();
const port = 1245;

// Redis client
const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

// List of products
const listProducts = [
    { id: 1, name: 'Suitcase 250', price: 50, stock: 4 },
    { id: 2, name: 'Suitcase 450', price: 100, stock: 10 },
    { id: 3, name: 'Suitcase 650', price: 350, stock: 2 },
    { id: 4, name: 'Suitcase 1050', price: 550, stock: 5 }
];

// Function to get item by ID
function getItemById(id) {
    return listProducts.find(product => product.id === id);
}

// Route to get the list of products
app.get('/list_products', (req, res) => {
    const products = listProducts.map(product => ({
        itemId: product.id,
        itemName: product.name,
        price: product.price,
        initialAvailableQuantity: product.stock
    }));
    res.json(products);
});

// Function to reserve stock by ID
async function reserveStockById(itemId, stock) {
    await setAsync(`item.${itemId}`, stock);
}

// Function to get current reserved stock by ID
async function getCurrentReservedStockById(itemId) {
    const stock = await getAsync(`item.${itemId}`);
    return stock ? parseInt(stock) : 0;
}

// Route to get the details of a product by ID
app.get('/list_products/:itemId', async (req, res) => {
    const itemId = parseInt(req.params.itemId);
    const product = getItemById(itemId);

    if (!product) {
        return res.json({ status: 'Product not found' });
    }

    const reservedStock = await getCurrentReservedStockById(itemId);
    const currentQuantity = product.stock - reservedStock;

    res.json({
        itemId: product.id,
        itemName: product.name,
        price: product.price,
        initialAvailableQuantity: product.stock,
        currentQuantity: currentQuantity
    });
});

// Route to reserve a product by ID
app.get('/reserve_product/:itemId', async (req, res) => {
    const itemId = parseInt(req.params.itemId);
    const product = getItemById(itemId);

    if (!product) {
        return res.json({ status: 'Product not found' });
    }

    const reservedStock = await getCurrentReservedStockById(itemId);
    const currentQuantity = product.stock - reservedStock;

    if (currentQuantity <= 0) {
        return res.json({ status: 'Not enough stock available', itemId: itemId });
    }

    await reserveStockById(itemId, reservedStock + 1);
    res.json({ status: 'Reservation confirmed', itemId: itemId });
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
