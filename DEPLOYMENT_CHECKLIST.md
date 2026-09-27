# Deployment Checklist

- [ ] Create GitHub repository.
- [ ] Push the project files.
- [ ] Confirm `.env` and database files are ignored.
- [ ] Connect the repository to Render.
- [ ] Build command: `pip install -r requirements.txt`
- [ ] Start command: `gunicorn app:app`
- [ ] Set `SECRET_KEY` in Render environment variables.
- [ ] Open the public URL.
- [ ] Verify `/health`.
- [ ] Verify vehicle listing.
- [ ] Create a demo booking.
- [ ] Verify confirmation and tracking.
- [ ] Record the public URL and screenshots in the Week 6 report.
