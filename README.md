# Auction Application

This repository contains an auction application developed using Django. The project enables users to list items for auction, place bids, and manage their watchlists, offering a platform for simulated auction functionality.

## Features

### User Authentication
- Sign-up, login, and logout functionalities.
- User accounts for tracking auctions, bids, and deals.

### Auction Management
- Users can create auctions with details such as category, title, description, price, and image.
- Categories include Fashion, Electronics, Food, Beverages, Furniture, and Media.

### Bidding System
- Users can place bids on auction items.
- Bids are validated to ensure they exceed the current price or the highest bid.

### Watchlist
- Add and remove items from a personal watchlist.
- Easily track auctions of interest.

### Comments
- Users can leave comments on auction items.

### Closed Deals
- Auctions can be closed by sellers, awarding the item to the highest bidder.
- Closed deals are recorded with details of the buyer, seller, and final price.

## Technologies Used

- **Backend Framework:** Django
- **Frontend:** HTML, CSS
- **Database:** SQLite
- **Authentication:** Django's built-in user model

```plaintext
auction_application/
├── manage.py               # Django management script
├── auction/                # Project configuration
│   ├── settings.py         # Project settings
│   ├── urls.py             # URL configurations
│   ├── wsgi.py             # WSGI configuration
│   └── asgi.py             # ASGI configuration
├── app/                    # Main application folder
│   ├── models.py           # Database models
│   ├── views.py            # Application views
│   ├── urls.py             # Application URL routes
│   ├── templates/          # HTML templates
│   └── static/             # CSS, JavaScript, and images
├── db.sqlite3              # SQLite database
├── requirements.txt        # Python dependencies
└── README.md               # Documentation
```
## Key Learning Outcomes

- Implementing user authentication and session management in Django.
- Building a bidding system with robust validation.
- Managing complex relationships between users, auctions, bids, and deals.
- Creating a scalable and modular application architecture.
