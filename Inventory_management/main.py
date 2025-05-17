from flask import Flask, render_template
from flask_cors import CORS
from product import product_bp, create_product_table
from location import location_bp, create_location_table
from movement import movement_bp, create_product_movements_table

def create_app():
    # Create the Flask app instance, setting static and template folders
    app = Flask(__name__, static_folder="static", template_folder="templates")
    CORS(app)

    # Register blueprints for API routes
    app.register_blueprint(product_bp, url_prefix="/api/products")
    app.register_blueprint(location_bp, url_prefix="/api/locations")
    app.register_blueprint(movement_bp, url_prefix="/api/movements")

    # Ensure tables exist BEFORE running the app
    with app.app_context():
        create_product_table()
        create_location_table()
        create_product_movements_table()  # Create the product movements table

    return app

# Create the app instance
app = create_app()

# Route to load the product page (main page)
@app.route('/')
def product_page():
    return render_template("product.html")

# Route to load the location page
@app.route('/locations')
def location_page():
    return render_template("location.html")

# Route to load the movement page (new movement page)
@app.route('/movements')
def movement_page():
    return render_template("movement.html")

# Run Flask application (you can switch off debug mode for production)
if __name__ == '__main__':
    app.run(debug=True)
