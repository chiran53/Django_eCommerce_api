# Django E-commerce API 

A RESTful API built with Django and Django REST Framework for managing products, carts, and orders in an e-commerce platform. This API supports secure user registration and authentication, product management, cart operations, and order processing with stock validation.

## Features ##

#### User Registration:

New users can register, automatically receive a cart, and are issued a token for authentication.

#### Product Management: 

Supports listing, viewing, and managing product details, including name, description, price and stock.

#### Cart Operations:

Users can add, update, and remove items in their cart.

#### Order Processing:

Allows users to place orders with cart items, ensuring stock validation and updating product stock after each purchase.

## Technologies

* Django - Backend framework.
* Django REST Framework - Used for creating RESTful APIs.
* Token-based Authentication - Used for secure user authentication.

## Installation and Setup

* Clone the Repository

git clone https://github.com/chiran53/Django_eCommerce_api.git
cd your-repo-name

* Create and Activate a Virtual Environment

python -m venv env

source env/bin/activate 

On Windows use `env\Scripts\activate`

* Install Dependencies

pip install -r requirements.txt

* Apply Migrations

python manage.py migrate

* Run the Server

python manage.py runserver

* Create a Superuser (for admin access)

python manage.py createsuperuser

## API Endpoints

* Here are the main API endpoints:

## Authentication

POST `/api-token-auth/`: Obtain authentication token.

## User Registration

POST `/api/register/`: Register a new user.

## Products

GET `/api/products/`: List all products.

POST `/api/products/`: Add a new product (Admin only).

GET `/api/products/{id}/`: Retrieve a single product's details.

## Cart

GET `/api/cart/`: View the user's cart.

POST `/api/cart/add/`: Add an item to the cart.

POST `/api/cart/remove/`: Remove an item from the cart.

## Orders

GET `/api/orders/`: List all user orders.

POST `/api/orders/place/`: Place an order with current cart items.

## Future Enhancements

* Payment Integration: Connect with payment gateways.
* Discounts and Promotions: Add discount codes and promotional pricing.
* Product Reviews: Allow users to review products.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## Feedback
If you have suggestions or feedback, please feel free to reach out or create an issue. Thank you for checking out the project!
