# Django E-Commerce Platform

A full-featured e-commerce web application built with Django.

## Features

### Authentication
- Custom User Model
- User Registration
- Email Verification
- Login / Logout
- JWT Authentication API

### Product Management
- Product Categories
- Product Search
- Product Details
- Pagination

### Shopping Cart
- Add / Remove Products
- Quantity Update
- Coupon Discounts
- Tax Calculation
- Session-based Cart

### Orders
- Order Creation
- Unique Order ID Generation
- Payment Proof Upload
- Order Confirmation Emails
- PDF Invoice Generation

### Coupons
- Discount Coupons
- Coupon Expiration Validation

### Async Tasks
- Celery Background Tasks
- RabbitMQ Message Broker
- Payment Completion Emails

### Performance
- Redis Product Caching

### Internationalization
- English / Arabic Support

### APIs
- Products API
- Categories API
- User Registration API
- Logout API
- Order API

### Containerization
- Docker
- Docker Compose
- PostgreSQL
- Redis
- RabbitMQ

---

## Tech Stack

- Django
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- RabbitMQ
- Docker
- WeasyPrint

---

## Project Structure

```bash
accounts/
store/
cart/
orders/
coupons/
apis/
templates/
media/
Dockerfile
docker-compose.yml
requirements.txt
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/django-ecommerce-platform.git
cd django-ecommerce-platform
```

Create `.env`

```env
SECRET_KEY=your_secret_key
DEBUG=True
EMAIL_HOST=your_host
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_password
EMAIL_PORT=587
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=your_email
```

Run:

```bash
docker compose up --build
```

Apply migrations:

```bash
docker compose exec web python manage.py migrate
```

Create superuser:

```bash
docker compose exec web python manage.py createsuperuser
```

Open:

```bash
http://localhost:8000
```

Admin panel:

```bash
http://localhost:8000/admin
```

RabbitMQ dashboard:

```bash
http://localhost:15672
```

---

## API Endpoints

### Authentication

```http
POST /api/token/
POST /api/token/refresh/
POST /v1/api/register/
POST /v1/api/logout/
```

### Products

```http
GET /v1/api/product/
GET /v1/api/product/<slug>
```

### Categories

```http
GET /v1/api/category/
GET /v1/api/category/<slug>
```

### Orders

```http
POST /orders/api/create/
```

---

## Future Improvements

- Better API permissions
- Payment gateway integration
- Automated payment verification
- Unit testing
- Deployment

---

## Author

**Moaz AbdelGhany**

Backend Developer (Django)
