from bikerepair import app


#with app.app_context():
#    db.create_all()
    #Service.default_table(db)


if __name__ == "__main__":
    app.run(debug=True)
