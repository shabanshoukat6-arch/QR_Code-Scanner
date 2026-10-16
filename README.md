# Gas Patrol Pump Payment -- QR Code Generator & Scanner

A Django web application for generating QR codes that contain
user-provided text and a 10-digit mobile number, then validating
uploaded QR images against records stored in the database. The project
uses OpenCV to decode QR images and SQLite to store generated QR
records.

## Features

-   Generate a QR code from text and a 10-digit mobile number.
-   Save generated QR images as PNG files.
-   Preview and download a generated QR code.
-   Upload a QR image for scanning and validation.
-   Verify that the QR content and submitted mobile number match a
    database record.
-   Delete the matching database record and generated QR image after a
    successful scan.
-   Remove the uploaded scan image after processing.
-   Shared navigation and styling using Django templates and CSS.

## Tech Stack

-   **Backend:** Python, Django 6.1.1
-   **Database:** SQLite
-   **QR generation:** `qrcode`
-   **QR decoding / image processing:** OpenCV, NumPy, Pillow
-   **Frontend:** HTML, CSS, Django Template Language

## Project Structure

``` text
Djangoqr/
├── core/
│   ├── static/core/css/style.css
│   ├── templates/core/
│   │   ├── base.html
│   │   └── home.html
│   ├── urls.py
│   └── views.py
├── djangoqr/
│   ├── settings.py
│   └── urls.py
├── scanner/
│   ├── migrations/
│   ├── templates/scanner/
│   │   ├── generate.html
│   │   └── scan.html
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── media/
│   ├── qr_codes/
│   └── uploads/
├── manage.py
└── requirements.txt
```

## Getting Started

### 1. Prerequisites

-   Python compatible with the installed Django and image-processing
    dependencies.
-   Git (optional, for cloning the repository).

### 2. Clone the repository

``` bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Djangoqr
```

Replace `<YOUR_GITHUB_REPOSITORY_URL>` with your repository URL. If you
downloaded the project instead, open a terminal in the folder containing
`manage.py`.

### 3. Create and activate a virtual environment

**Windows PowerShell:**

``` powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

``` bat
py -m venv venv
venv\Scripts\activate.bat
```

**macOS / Linux:**

``` bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install dependencies

``` bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Apply database migrations

``` bash
python manage.py migrate
```

### 6. Run the development server

``` bash
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in your browser.

## Application URLs

  Page           URL               Purpose
  -------------- ----------------- ---------------------------------
  Home           `/`               Project home page
  Generate QR    `/qr/generate/`   Generate and download a QR code
  Scan QR        `/qr/scan/`       Upload and validate a QR image
  Django Admin   `/admin/`         Django administration site

## How It Works

### Generate a QR code

1.  Open `/qr/generate/`.
2.  Enter a 10-digit mobile number and the text to encode.
3.  Submit the form.
4.  The application creates QR content in the format
    `text|mobile_number`, generates a PNG image, saves the text and
    mobile number in the database, and displays a download link.

### Scan and validate a QR code

1.  Open `/qr/scan/`.
2.  Enter the same 10-digit mobile number used during generation.
3.  Upload the corresponding QR image.
4.  OpenCV attempts to decode the QR image. The application checks the
    decoded text and number against the database record.
5.  If the record and submitted number match, the application reports
    success and removes the matched record and generated QR image. The
    uploaded scan image is removed after processing.

## Data Model

The `QRcode` model in `scanner/models.py` stores:

  -----------------------------------------------------------------------------
  Field                   Type                          Description
  ----------------------- ----------------------------- -----------------------
  `data`                  `CharField(max_length=255)`   Text encoded in the QR
                                                        code

  `mobile_number`         `CharField(max_length=10)`    Associated 10-digit
                                                        mobile number
  -----------------------------------------------------------------------------

## Important Notes

-   This project is configured for **local development**, not production
    deployment.
-   Before deploying, move `SECRET_KEY` into an environment variable,
    set `DEBUG = False`, configure `ALLOWED_HOSTS`, and configure secure
    media uploads and HTTPS.
-   Do not commit your virtual environment, local database, generated QR
    images, uploaded files, or private settings to GitHub unless you
    intentionally want to share them. Add suitable entries to
    `.gitignore`.
-   The scan template should include a visible submit button so users
    can submit the upload form easily.
-   The current implementation treats a successful scan as a one-time
    validation by deleting the matching record and generated QR image.

## Future Improvements

-   Add a visible submit button and clearer validation messages to the
    scan page.
-   Add automated tests for QR generation, invalid input, and scan
    validation.
-   Improve upload validation and limit permitted image types and file
    sizes.
-   Add authentication and a history page if the application needs
    multiple users.
-   Add a proper production deployment configuration.

## License

No license is currently specified. Add a `LICENSE` file before allowing
others to reuse, modify, or distribute this project under defined terms.
