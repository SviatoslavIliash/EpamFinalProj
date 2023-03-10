"""Main start point for application"""
from bikerepair import create_app, db
#from bikerepair.models import Service

app = create_app('DEVELOP')
#with app.app_context():
#    db.create_all()
#    Service.default_table(db)


if __name__ == "__main__":
    app.run(debug=True)
