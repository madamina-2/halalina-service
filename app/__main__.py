from app import create_app

# Create Flask app using the factory function
app = create_app()

# Run the app if this file is executed
if __name__ == '__main__':
    app.run(debug=True)  # or use app.run() without debug in production
