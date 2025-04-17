from app import create_app, db
from app.models.seeder import seed_job_types  # Import the seed function

# Create Flask app using the factory function
app = create_app()

@app.cli.command("seed")
def seed():
    """Mengisi tabel dengan data awal (seeding)."""
    print("Seeding job types...")
    seed_job_types()
    db.session.commit()
    print("Seeder selesai!")

# Run the app if this file is executed
if __name__ == '__main__':
    app.run(debug=True)  # or use app.run() without debug in production
