import axios from 'axios';

export const apiDjango = axios.create({
    baseURL: 'http://localhost:8001/api',
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json',
    },
});
