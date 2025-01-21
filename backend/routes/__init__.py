def register_routes(app):
    from .disaster_routes import disaster_bp
    from .prediction_routes import prediction_bp
    from .weather_routes import weather_bp
    
    app.register_blueprint(disaster_bp)
    app.register_blueprint(prediction_bp)
    app.register_blueprint(weather_bp)