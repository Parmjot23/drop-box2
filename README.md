# Local Dropbox

This project is a lightweight Django application for sharing files on a local network.  
Uploaded files are stored on the server and can be browsed from any authenticated device on the same LAN.

## Features

* **File upload and download** – Upload multiple files and access them from the browser.
* **Folder organisation** – Create folders and assign uploaded files to them.
* **Image and video previews** – Thumbnails are generated for images and videos for quick browsing.
* **Search** – Search by file title, type and upload date.
* **Authentication** – Login is required to access any view.
* **Refresh button** – Quickly reload the page to see new files.
* **Comments** – Leave notes on individual files for collaboration.

Additional functionality such as LAN device discovery or peer‑to‑peer sync is not included.

## Development

Create migrations and run the server:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

Media files are stored in the `media/` directory and static files in `staticfiles/`.
