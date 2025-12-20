# Paws a Moment Rescue - Django Web Application

A comprehensive Django-powered web application for managing a pet adoption and rescue service.

## Features

- **Animal Profile Management**: Create, edit, archive, and delete animal profiles with image galleries
- **Adoption & Foster Applications**: Accept and manage adoption and foster applications
- **Contact Form**: Email relay for contact messages
- **News Management**: Publish news articles with expiry dates
- **Admin Dashboard**: Statistics and analytics dashboard
- **CSV Export**: Export all data types to CSV
- **Image Processing**: Automatic square image processing with #f5f5f5 background bars
- **Filtering**: Advanced filtering for adoption list (species, size, sex, search)
- **Visit Tracking**: Automatic tracking of site visits and animal profile views

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Migrations

```bash
python manage.py migrate
```

### 3. Create Superuser

```bash
python manage.py createsuperuser
```

### 4. Configure Email Settings

Edit `pawsamoment/settings.py` and set:
- `EMAIL_HOST_PASSWORD`: Your email password (or use environment variables)
- For Gmail, you may need to use an "App Password" instead of your regular password

### 5. Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to see the site.

## Admin Access

- Access admin panel at: `http://127.0.0.1:8000/admin/`
- Use the superuser credentials you created
- Regular admin users can be created through the admin panel (they won't have delete permissions for other users)

## Key URLs

- Home: `/`
- Animals: `/animals/`
- Adoption Application: `/applications/adoption/`
- Foster Application: `/applications/foster/`
- Contact: `/contact/`
- News: `/news/`
- Dashboard: `/dashboard/` (staff only)

## Image Upload

When uploading animal images:
- Images are automatically processed to be square (max 1000x1000px)
- Non-square images get #f5f5f5 background bars
- Images are converted to JPEG format

## CSV Export

CSV exports are available:
- From the admin panel (select items and use "Export Selected as CSV")
- From the dashboard page (bulk exports)

## Notes

- The middleware automatically tracks site visits and animal views
- Archived animals are hidden from public listings but remain in the database
- News articles with expiry dates are automatically hidden after expiry
- Email functionality requires proper SMTP configuration

## Production Deployment

For production:
1. Set `DEBUG = False` in settings.py
2. Set `ALLOWED_HOSTS` appropriately
3. Use a production database (PostgreSQL recommended)
4. Configure proper static file serving
5. Set up environment variables for sensitive data
6. Use a production email service (SendGrid, AWS SES, etc.)

