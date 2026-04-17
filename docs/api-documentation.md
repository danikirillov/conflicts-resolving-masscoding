# Pet Shop API Documentation

This document provides comprehensive information about the Pet Shop REST API.

## Base URL

```
Development: http://localhost:3000/api
Staging: https://staging-api.petshop.com/api
Production: https://api.petshop.com/api
```

## Authentication

Most endpoints require authentication using JWT tokens.

### Login

```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

Response:
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

### Using the Token

Include the token in the Authorization header:

```http
Authorization: Bearer YOUR_JWT_TOKEN
```

## Endpoints

### Products

#### Get All Products

```http
GET /products
```

Query Parameters:
- `category` (string): Filter by category
- `minPrice` (number): Minimum price
- `maxPrice` (number): Maximum price
- `page` (number): Page number (default: 1)
- `limit` (number): Items per page (default: 20)

Response:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Golden Retriever Puppy",
      "species": "Dog",
      "breed": "Golden Retriever",
      "age": 3,
      "price": 800.00,
      "image": "https://cdn.petshop.com/images/golden-retriever.jpg"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150
  }
}
```

#### Get Product by ID

```http
GET /products/:id
```

Response:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Golden Retriever Puppy",
    "species": "Dog",
    "breed": "Golden Retriever",
    "age": 3,
    "price": 800.00,
    "description": "Friendly and energetic puppy...",
    "image": "https://cdn.petshop.com/images/golden-retriever.jpg",
    "vaccinated": true,
    "health_records": []
  }
}
```

### Orders

#### Create Order

```http
POST /orders
Authorization: Bearer TOKEN
Content-Type: application/json

{
  "items": [
    {
      "product_id": 1,
      "quantity": 1
    }
  ],
  "shipping_address": {
    "street": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zip": "10001"
  }
}
```

Response:
```json
{
  "success": true,
  "order_id": 1234,
  "total": 864.00,
  "status": "pending"
}
```

#### Get Order by ID

```http
GET /orders/:id
Authorization: Bearer TOKEN
```

#### Get User Orders

```http
GET /users/me/orders
Authorization: Bearer TOKEN
```

### Users

#### Register User

```http
POST /auth/register
Content-Type: application/json

{
  "email": "newuser@example.com",
  "password": "securepassword",
  "name": "Jane Doe"
}
```

#### Get Current User

```http
GET /users/me
Authorization: Bearer TOKEN
```

#### Update User Profile

```http
PUT /users/me
Authorization: Bearer TOKEN
Content-Type: application/json

{
  "name": "Jane Smith",
  "phone": "555-0123"
}
```

### Cart

#### Add to Cart

```http
POST /cart/items
Authorization: Bearer TOKEN
Content-Type: application/json

{
  "product_id": 1,
  "quantity": 1
}
```

#### Get Cart

```http
GET /cart
Authorization: Bearer TOKEN
```

#### Update Cart Item

```http
PUT /cart/items/:product_id
Authorization: Bearer TOKEN
Content-Type: application/json

{
  "quantity": 2
}
```

#### Remove from Cart

```http
DELETE /cart/items/:product_id
Authorization: Bearer TOKEN
```

## Error Handling

All endpoints return errors in the following format:

```json
{
  "success": false,
  "error": {
    "code": "INVALID_INPUT",
    "message": "Email is required"
  }
}
```

### Error Codes

- `INVALID_INPUT`: Invalid request data
- `UNAUTHORIZED`: Authentication required
- `FORBIDDEN`: Insufficient permissions
- `NOT_FOUND`: Resource not found
- `INTERNAL_ERROR`: Server error

## Rate Limiting

API requests are limited to:
- 100 requests per minute (authenticated)
- 20 requests per minute (unauthenticated)

Rate limit info is included in response headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1234567890
```

## Webhooks

Subscribe to events:
- `order.created`
- `order.shipped`
- `payment.completed`

Configure webhooks in your account settings.

## SDK Examples

### JavaScript

```javascript
const petshop = require('@petshop/sdk');

const client = petshop.createClient({
  apiKey: 'YOUR_API_KEY'
});

// Get products
const products = await client.products.list();

// Create order
const order = await client.orders.create({
  items: [{ product_id: 1, quantity: 1 }]
});
```

### Python

```python
from petshop import Client

client = Client(api_key='YOUR_API_KEY')

# Get products
products = client.products.list()

# Create order
order = client.orders.create(
    items=[{'product_id': 1, 'quantity': 1}]
)
```

## Support

For API support:
- Email: api@petshop.com
- Documentation: https://docs.petshop.com
- Status Page: https://status.petshop.com
