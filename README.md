# Phone OTP Authentication System

This Django REST API backend provides a phone number-based OTP (One-Time Password) authentication system. Users can register and login using their phone numbers, with verification done through SMS OTP.

## Features

- Phone number-based authentication with SMS OTP verification
- User registration with profile information (name, email, phone number, date of birth)
- Newsletter subscription option
- Mobile device token storage for push notifications
- Session-based authentication

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

```bash
python manage.py migrate
```

### 4. Start Development Server

```bash
python manage.py runserver
```

## Twilio Integration

This system uses Twilio for sending SMS OTPs. You need to:

1. Sign up for a [Twilio account](https://www.twilio.com/try-twilio)
2. Get your Account SID and Auth Token from the Twilio Console
3. Purchase or use a trial phone number
4. Add these values to your `.env` file:

```
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
```

## API Endpoints

### Authentication

- `POST /api/auth/register/` - Register a new user
- `POST /api/auth/login/send-otp/` - Request an OTP for login
- `POST /api/auth/login/verify-otp/` - Verify OTP and login
- `POST /api/auth/logout/` - Logout current user

### User Information

- `GET /api/auth/users/me/` - Get current user information
- `PATCH /api/auth/users/me/` - Update current user information
- `POST /api/auth/users/update_device_token/` - Update device token for push notifications

## Development Mode

If Twilio credentials are not configured, the system will work in development mode:
- OTPs are returned in the API response
- A warning message is shown indicating SMS sending failed 