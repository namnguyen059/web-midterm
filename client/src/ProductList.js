import React, { useState, useEffect } from "react";
import axios from "axios";

const ProductList = () => {
  const [products, setProducts] = useState([]); // State for product data
  const [error, setError] = useState(""); // State for error handling
  const [loading, setLoading] = useState(true); // State for loading state

  useEffect(() => {
    // Fetch products from API
    const fetchProducts = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/products/");
        setProducts(response.data); // Update state with products
        setLoading(false); // Set loading to false after data is loaded
      } catch (err) {
        setError("Failed to fetch products.");
        setLoading(false); // Set loading to false on error
      }
    };
    fetchProducts();
  }, []);

  if (loading) return <p>Loading products...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div>
      <h1>Product List</h1>
      <ul>
        {products.map((product) => (
          <li key={product._id}>
            <h2>{product.name}</h2>
            <p>{product.description}</p>
            <p>Category: {product.category}</p>
            <p>Price: ${product.price.toFixed(2)}</p>
            <p>Stock: {product.stock}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ProductList;
