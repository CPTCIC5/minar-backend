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

## MSG91 Integration for SMS OTP

This system uses MSG91 for sending SMS OTPs, which works well in India. You need to:

1. Sign up for a [MSG91 account](https://msg91.com/)
2. Create an OTP template in MSG91 dashboard with a variable for the OTP code
3. Get your Auth Key and Template ID from the MSG91 dashboard
4. Add these values to your `.env` file:

```
MSG91_AUTH_KEY=your_msg91_auth_key
MSG91_TEMPLATE_ID=your_msg91_template_id
MSG91_SENDER_ID=OTPSMS  # You can customize this
```

### Creating an OTP Template in MSG91
When creating a template in MSG91, make sure to include the variable `{{otp}}` in your message. 
Example template: "Your verification code is {{otp}}. Valid for 10 minutes."

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

If MSG91 credentials are not configured, the system will work in development mode:
- OTPs are returned in the API response
- A warning message is shown indicating SMS sending failed 