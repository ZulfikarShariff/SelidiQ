# selidiq/app.py

from selidiq import create_app

# Initialize the application
app = create_app()

# Run the application only if this file is executed directly
if __name__ == '__main__':
    # Run in debug mode for development purposes
    app.run(host="0.0.0.0", port=5002)

