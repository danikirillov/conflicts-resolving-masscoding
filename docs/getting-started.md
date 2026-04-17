# Getting Started with Pet Shop

Welcome to the Pet Shop application! This guide will help you set up and run the project locally.

## Prerequisites

Before you begin, ensure you have the following installed:
- Node.js (v18 or higher)
- PostgreSQL (v15 or higher)
- Redis
- Docker (optional, for containerized setup)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/pet-shop.git
cd pet-shop
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
DATABASE_URL=postgresql://postgres:password@localhost:5432/petshop
REDIS_URL=redis://localhost:6379
PORT=3000
NODE_ENV=development
```

### 4. Set Up the Database

Run database migrations:

```bash
npm run migrate
```

Seed initial data:

```bash
npm run seed
```

### 5. Start the Application

Development mode:
```bash
npm run dev
```

Production mode:
```bash
npm start
```

The application will be available at `http://localhost:3000`

## Docker Setup

If you prefer using Docker:

```bash
docker-compose up -d
```

This will start all required services (web, database, redis, nginx).

## Project Structure

```
pet-shop/
├── frontend/          # Frontend code (JavaScript, PHP)
├── backend/           # Backend services (Java, Python, C++)
├── html/              # HTML templates
├── devops/            # DevOps configurations
├── docs/              # Documentation
└── tests/             # Test files
```

## Next Steps

- Read the [User Guide](user-guide.md) for usage instructions
- Check out the [API Documentation](api-documentation.md)
- Review the [Deployment Guide](deployment-guide.md) for production setup

## Troubleshooting

If you encounter any issues, refer to the [Troubleshooting Guide](troubleshooting.md).

## Support

For questions or support:
- Email: support@petshop.com
- GitHub Issues: https://github.com/yourusername/pet-shop/issues
