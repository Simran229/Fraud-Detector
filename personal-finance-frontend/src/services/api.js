import axios from 'axios';

const API = axios.create({
    baseURL: 'http://127.0.0.1:5000/api', // Your Flask backend
});

// Example: Register User
export const registerUser = (userData) => API.post('/register', userData);

// Example: Login User
export const loginUser = (userData) => API.post('/login', userData);

// Example: Add Transaction
export const addTransaction = (transactionData, token) => 
    API.post('/transactions', transactionData, {
        headers: { Authorization: `Bearer ${token}` }
    });
