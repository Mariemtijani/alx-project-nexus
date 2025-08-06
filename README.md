# alx-project-nexus

## Overview of the ProDev Backend Engineering Program
This repository documents my journey and learnings from the **ProDev Backend Engineering program** at ALX. It showcases backend engineering concepts, tools, and best practices applied in building a production-grade backend project.

For this program, I chose to develop an **E-Commerce Platform for Moroccan Artisans and Associations**. The platform aims to empower artisans to showcase and sell their handcrafted products online, manage operations efficiently, and reach national and international buyers.

---

## Key Technologies Covered
- **Python 3.11**
- **Django 5.x**
- **GraphQL API (Graphene-Django)**
- **PostgreSQL**
- **Docker & Docker Compose**
- **JWT Authentication (django-graphql-jwt)**
- **CI/CD Pipelines (GitHub Actions - planned)**

---

## Important Backend Development Concepts
- **Database Design & Entity Relationship Diagrams (ERD)**
  - Modularized models: User, Association, Artisan, Product, Order, Payment, Review, Favorite (Wishlist)
  - Polymorphic relationships: Product ownership by either Artisan or Association
  - Multilingual product descriptions using Translation models

- **GraphQL API Design**
  - Modular schema architecture (apps: users, products, orders, associations)
  - Clean Query & Mutation separation per domain
  - Structured Input types for complex mutations (e.g., OrderItemInput)
  - Role-based permissions using decorators and contextual access control

- **Authentication & Authorization**
  - JWT-based login, registration, and token refreshing
  - Secure password hashing with bcrypt (passlib)
  - Role-based access control integrated in mutation resolvers

- **Asynchronous Programming (Planned)**
  - Task queues for sending emails, order notifications (using Celery)

- **Caching Strategies (Planned)**
  - Redis caching for product listings and common GraphQL queries

---

## Challenges Faced & Solutions Implemented
 Challenge                                         Solution 

Complex relationships between Artisan, Association, Product ===>  Designed a clean ERD with strict FK constraints and polymorphic ownership | Keeping GraphQL Schema modular and maintainable   ===>  Created per-domain schema files and aggregated them in app-level __init__.py |
Securing sensitive mutations          ===>            Applied @login_required and custom role-based decorators |
PostgreSQL connectivity in Docker      ===>           Fixed with proper network aliases and environment configs |
 Handling multilingual product content     ===>        Created a Translation model linked to Product |

---

## Best Practices and Personal Takeaways
- **Structure early, scale easier**: Modular folders & schema help in big projects.
- **Secure mutations from the start**: Protect every sensitive action.
- **Plan ERD deeply before coding**: Saves massive refactoring later.
- **Automate dev environment using Docker**: No more “it works on my machine”.
- **Focus on API design clarity**: GraphQL inputs make mutations maintainable.
- **Self-discipline when solo building**: Documentation & organization are key.
- **Role-based access must be dynamic**: Especially in multi-role apps like e-commerce platforms.

---

## Repository Structure
alx-project-nexus/
├── app/
│ ├── core/
│ ├── users/
│ ├── associations/
│ ├── products/
│ ├── orders/
│ └── settings.py
├── docker-compose.yml
├── Dockerfile
├── .env
├── requirements.txt
└── README.md


---

## Future Enhancements
- CI/CD Pipelines using GitHub Actions
- Frontend Integration (via GraphQL endpoints)
- Asynchronous background tasks (emails, notifications)
- Redis caching layer for performance
- Deploying to production (DigitalOcean or AWS EC2)

---

## Personal Reflection
Building this platform as a solo backend developer has been a deep dive into real-world architecture and professional development workflows. I applied backend fundamentals in a production-like environment, structured code for scalability, and prioritized API security and clean design. It was a challenging but rewarding learning experience.

