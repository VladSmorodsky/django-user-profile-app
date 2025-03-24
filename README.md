# django-user-profile-app

It's user profile management system that allows users to register, edit their profile, change their password, and view
other users' profiles. Users can sign in with Google account.

## Project Setup

1. Clone the repo
2. Change working dir to project root:

```shell
cd user_profile
```

3. Copy `user_profile/.env.example` file and enter values into `user_profile/.env` file:

- **PROJECT_SECRET_KEY** - project secret key
- **GOOGLE_CLIENT_ID** - client id from Google Web application
- **GOOGLE_CLIENT_SECRET** - client secret from Google Web application

4. Run migrations

```shell
python manage.py migrate
```

5. Create superuser:

```shell
python manage.python creaetesuperuser
```

6. Run server:

```shell
python manage.py runserver
```

## Social accounts

Project uses [`django-allauth`](https://docs.allauth.org/en/latest/) package. There is only Google provider
implementation in the application.