"""Main start point for application"""
from bikerepair import create_app, db
import logging


app = create_app('DEVELOP')


if __name__ == "__main__":
    app.run(debug=True)
