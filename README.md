# CareLink - Hackathon Submission

## Quickstart (local)

1. Copy `.env.example` to `.env` and set DB credentials.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Import the database:
   ```bash
   mysql -u root -p carelink < carelink.sql
   ```
4. Run the app:
   ```bash
   python app.py
   ```
5. Seed demo data (optional):
   ```bash
   python seed_data.py
   ```

API endpoints are available under `http://127.0.0.1:5000/`.
