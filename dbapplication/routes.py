import dbapplication.db_manager as dbm


def register_routes(app, db):

    @app.route("/add/customer", methods=['POST'])
    def add_customer():
        return dbm.new_customer(db)

    @app.route("/add/reservation", methods=['POST'])
    def add_reservation():
        return dbm.new_reservation(db)

    @app.route("/add/restaurant", methods=['POST'])
    def add_restaurant():
        return dbm.new_restaurant(db)

    @app.route("/add/manager", methods=['POST'])
    def add_manager():
        return dbm.new_manager(db)

    @app.route("/add/partner_company", methods=['POST'])
    def add_partner_company():
        return dbm.new_partner_company(db)

    @app.route("/get/seats", methods=['GET'])
    def check_available_seats():
        return dbm.available_seats(db)

    @app.route("/get/reservation/<string:date>", methods=['GET'])
    def get_reservation_by_date(date):
        return dbm.reservation_by_date(db, date)

    @app.route("/get/reservation/<int:id>", methods=['GET'])
    def get_reservation_by_id(id):
        return dbm.reservation_by_id(id)

    @app.route("/get/reservation/company/<int:id>", methods=['GET'])
    def get_reservation_by_company(id):
        return dbm.reservation_by_company(id)

    @app.route("/get/reservation/customer/<int:id>", methods=['GET'])
    def get_reservation_by_customer(id):
        return dbm.reservation_by_customer(id)

    @app.route("/update/customer", methods=['POST'])
    def change_customer_discount():
        return dbm.change_discount_customer(db)

    @app.route("/update/company", methods=['POST'])
    def change_company_discount():
        return dbm.change_discount_company(db)

    @app.route("/update/reservation/confirm/<int:id>", methods=['POST'])
    def confirm_reservation(id):
        return dbm.confirm_reservation(db, id)

    @app.route("/update/reservation/cancel/<int:id>", methods=['POST'])
    def cancel_reservation(id):
        return dbm.cancel_reservation(db, id)

    @app.route("/update/reservation/complete/<int:id>", methods=['POST'])
    def complete_reservation(id):
        return dbm.complete_reservation(db, id)
