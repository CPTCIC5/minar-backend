# Email Verification Authentication System

This Django REST API backend provides an email verification-based authentication system. Users register with email/password and receive a verification email before they can login.

## Features

- Email verification-based authentication
- User registration with profile information (name, email, phone number, date of birth)
- Newsletter subscription option
- Mobile device token storage for push notifications
- Session-based authentication
- Password reset via email

## Setup

### 1. Environment Setup

Copy the `.env.example` file to `.env` and update the values:

```bash
cp .env.example .env
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Migrations

First, you'll need to create the initial migration files:

```bash
python manage.py makemigrations users
```

Then apply the migrations:

```bash
python manage.py migrate
```

### 4. Create a Superuser

Create an admin user to manage the application:

```bash
python manage.py createsuperuser
```

### 5. Start Development Server

```bash
python manage.py runserver
```

## Email Configuration

This system sends verification emails using Django's email system. You need to configure:

1. Email server settings in `.env` file:
```
EMAIL_HOST=smtp.elasticemail.com
EMAIL_PORT=2525
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_email_password
```

2. Frontend URL for verification links:
```
FRONTEND_URL=https://your-frontend-url.com
```

## API Endpoints

### Authentication

- `POST /api/auth/register/` - Register a new user
- `POST /api/auth/verify-email/` - Verify email using token
- `POST /api/auth/login/` - Login with email and password
- `POST /api/auth/logout/` - Logout current user

### Password Management

- `POST /api/auth/password/reset-request/` - Request password reset
- `POST /api/auth/password/reset-confirm/` - Reset password with token
- `POST /api/auth/password/change/` - Change password (when logged in)

### User Information

- `GET /api/auth/users/me/` - Get current user information
- `PATCH /api/auth/users/me/` - Update current user information
- `POST /api/auth/users/update_device_token/` - Update device token for push notifications

## Authentication Flow

1. User registers with email, phone number, and other required information
2. System sends a verification email with a unique token
3. User clicks the verification link to verify their email
4. After verification, user can log in with email and password
5. Failed login attempts with unverified emails will trigger resending of verification emails 