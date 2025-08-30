# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a FastAPI-based E-commerce backend API with JWT authentication, Redis caching, PostgreSQL database, and comprehensive testing. The architecture follows clean separation with models, services, schemas, and API routers.

## Development Commands

### Environment Setup
```bash
# Start all services (FastAPI app, PostgreSQL, Redis)
docker-compose up -d

# Build and start with fresh containers
docker-compose up -d --build

# Initialize database with sample data (first-time setup only)
docker-compose exec db psql -U postgres -d app -f /docker-entrypoint-initdb.d/seed.sql

# Stop all services
docker-compose down
```

### Testing
```bash
# Run all tests
docker-compose exec web pytest -v

# Run specific test file
docker-compose exec web pytest app/tests/test_routes.py -v

# Run tests with coverage
docker-compose exec web pytest app/tests/ --cov=app --cov-report=term-missing
```

### Database Operations
```bash
# Access database directly
docker-compose exec db psql -U postgres -d app

# Generate new migration
docker-compose exec web alembic revision --autogenerate -m "migration_description"

# Apply migrations
docker-compose exec web alembic upgrade head

# View migration history
docker-compose exec web alembic history
```

### Development Utilities
```bash
# View application logs
docker-compose logs web

# Execute commands inside the web container
docker-compose exec web bash

# Clear Redis cache
docker-compose exec redis redis-cli FLUSHALL
```

## Architecture Overview

### Core Structure
- **FastAPI Application**: Modern async web framework with automatic OpenAPI documentation
- **SQLAlchemy 2.0**: Modern ORM with full type annotation support and relationship management
- **Redis Caching**: Performance optimization layer for product queries with TTL-based invalidation
- **JWT Authentication**: OAuth2 password flow with admin/user role separation
- **Pydantic Schemas**: Request/response validation with custom validators
- **Docker Containerization**: Full development environment with PostgreSQL, Redis, and FastAPI

### Database Models & Relationships
The system implements a comprehensive e-commerce data model:

**User System**:
- Users with admin flag for authorization
- One-to-many relationships with addresses and phone numbers
- JWT token-based authentication with bcrypt password hashing

**Product Catalog**:
- Products with categories, units (KG/G/LITER/PIECE), stock management
- Product images relationship (one-to-many)
- Price and stock constraints at database level

**Shopping Cart**:
- One-to-one user-cart relationship
- Many-to-many products through CartItem junction table

**Planned Extensions** (from plan file):
- Order management with payment integration
- Product reviews system
- Advanced address and phone number handling

### Service Layer Architecture
Business logic is encapsulated in services with clear responsibilities:

- **User Services**: Registration, authentication, token management
- **Product Services**: CRUD operations with Redis caching integration
- **Cart Services**: Shopping cart management
- **Utils**: Shared utilities and helper functions

### Authentication & Authorization
- **JWT Tokens**: 30-minute expiration (configurable via TOKEN_LIFESPAN)
- **OAuth2 Password Flow**: Standard bearer token authentication
- **Role-Based Access**: Admin-only endpoints for product management
- **Dependency Injection**: Clean separation with `get_current_user` and `get_admin_user` dependencies

### Caching Strategy
Redis caching is implemented with intelligent invalidation:
- **Product Lists**: Cached with query parameters as keys (10-minute TTL)
- **Individual Products**: Cached by ID (10-minute TTL)
- **Cache Invalidation**: Automatic on product creation/updates
- **Pattern Deletion**: Bulk cache clearing for related keys

### Testing Approach
The test suite emphasizes parameterized testing and authentication verification:
- **Parameterized Tests**: Multiple input scenarios tested efficiently
- **Authentication Tests**: Protected routes properly reject unauthorized requests
- **TestClient Integration**: FastAPI test client for full integration testing

## Configuration

### Development Settings
Configuration is centralized in `app/core/config.py`:
- Database URL points to Docker container (`postgresql://postgres:changethis@db/app`)
- JWT secret key and algorithm configuration
- Token lifespan and development flags

### Environment Variables
For production deployments, create an `.env` file with:
```env
DATABASE_URL=postgresql://user:strongpassword@hostname/dbname
SECRET_KEY=your-super-secret-key-here
```

## API Endpoints

The API provides comprehensive e-commerce functionality:

**Authentication**:
- `POST /register` - User registration with validation
- `POST /login` - JWT token authentication

**Products** (public endpoints with optional authentication for admin operations):
- `GET /products/` - List products with search and pagination
- `GET /products/{id}` - Product details
- `POST /products/` - Create product (admin only)
- `PATCH /products/{id}/` - Update product (admin only)
- `DELETE /products/{id}/` - Delete product (admin only)

**Shopping Cart** (authenticated endpoints):
- `GET /cart/` - Get user's cart contents
- `POST /cart/add/` - Add items to cart

## Database Schema Notes

### Product Units Enum
The `UnitEnum` defines valid measurement units:
- `KG` - Kilograms
- `G` - Grams (mapped from "GRAM")
- `LITER` - Liters
- `PIECE` - Individual items

### Constraints
Database-level constraints ensure data integrity:
- Product prices must be >= 0
- Stock levels must be >= 0
- Unique product names
- Foreign key relationships enforced

## Development Best Practices

### Code Organization
- Models define database structure with SQLAlchemy
- Schemas handle request/response validation with Pydantic
- Services contain business logic and database operations
- API routers handle HTTP concerns and dependency injection

### Error Handling
- HTTPExceptions with appropriate status codes
- Comprehensive validation at schema level
- Database constraint violations properly handled

### Performance Considerations
- Redis caching reduces database load for frequent queries
- Connection pooling configured for PostgreSQL
- Parameterized queries prevent SQL injection
