from sqlalchemy import Date, cast, func

from flask import request, jsonify

from dbapplication.models import Customer, Restaurant, Manager, Reservation, PartnerCompany
from dbapplication.models.reservation_status import ReservationStatus
from datetime import datetime



def check_available_space(db, date, restaurant_id, guest_count):
    total_reserved = db.session.query(func.sum(Reservation.guest_number)) \
        .filter(Reservation.restaurant_id == restaurant_id,
                Reservation.reservation_status != ReservationStatus.CANCELLED.value,
                func.date(Reservation.date) == date.date())
    total_reserved = total_reserved.scalar() or 0
    restaurant = Restaurant.query.get(restaurant_id)
    available_seats = restaurant.total_guest_number - total_reserved

    if available_seats < guest_count:
        return jsonify({"error": f"Not enough seats available at {date}"}), 409

    return None



def check_restaurant(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 400


def check_reservation_owner(db, customer_id, partner_company_id):
    customer = db.session.get(Customer, customer_id)
    partner_company = db.session.get(PartnerCompany, partner_company_id)
    if not customer and not partner_company:
        return jsonify({"error": "Restaurant or customer not found"}), 400

def check_manager(db, manager_id):
    manager = db.session.get(Manager, manager_id)
    if manager is None:
        return jsonify({"error": "Manager not found"}), 400


def check_customer(db, customer_id):
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 400


def check_company(db, manager_id):
    manager = db.session.get(PartnerCompany, manager_id)
    if not manager:
        return jsonify({"error": "Partner company not found"}), 400


def new_reservation(db):
    restaurant_id = int(request.form.get("restaurant_id")) if request.form.get("restaurant_id") else None
    customer_id = int(request.form.get("customer_id")) if request.form.get("customer_id") else None
    partner_company_id = int(request.form.get("partner_company_id")) if request.form.get("partner_company_id") else None
    date_str = request.form.get("date")
    try:
        new_date = datetime.strptime(date_str, "%d.%m.%Y %H:%M")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use DD.MM.YYYY HH:MM"}), 400

    guests = request.form.get("guest_number")
    restaurant_check = check_restaurant(restaurant_id)
    if restaurant_check:
        return restaurant_check
    owner_check = check_reservation_owner(db, customer_id, partner_company_id)
    if owner_check:
        return owner_check
    space_check = check_available_space(db, new_date, restaurant_id, int(guests))
    if space_check:
        return space_check
    try:
        reservation = Reservation(
            restaurant_id=restaurant_id,
            customer_id=customer_id,
            partner_company_id=partner_company_id,
            date=new_date,
            reservation_name=request.form.get("reservation_name"),
            guest_number=guests,
            allergies=request.form.get("allergies"),
            total_cost=0,
            reservation_status=ReservationStatus.PENDING.value

        )
        db.session.add(reservation)
        db.session.commit()
        return jsonify({"message": "Reservation added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


def new_customer(db):
    try:
        customer = Customer(
            name=request.form.get("name"),
            email=request.form.get("email"),
            discount=request.form.get("discount"),
        )
        db.session.add(customer)
        db.session.commit()
        return jsonify({"message": "Customer added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


def new_restaurant(db):
    manager_id = request.form.get("manager_id")
    manager_check =check_manager(db, manager_id)
    if manager_check:
        return manager_check
    try:
        restaurant = Restaurant(
            manager_id=manager_id,
            name=request.form.get("name"),
            city=request.form.get("city"),
            total_guest_number=request.form.get("total_guest_number")

        )
        db.session.add(restaurant)
        db.session.commit()
        return jsonify({"message": "Restaurant added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


def new_manager(db):
    try:
        manager = Manager(
            name=request.form.get("name"),
            email=request.form.get("email"),
            city=request.form.get("city"),
        )
        db.session.add(manager)
        db.session.commit()
        return jsonify({"message": "Manager added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


def new_partner_company(db):
    try:
        new_partner = PartnerCompany(
            name=request.form.get("name"),
            email=request.form.get("email"),
            discount=request.form.get("discount"),
        )
        db.session.add(new_partner)
        db.session.commit()
        return jsonify({"message": "Partner company added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


def available_seats(db):
    print()
    restaurant_id = int(request.form.get("restaurant_id")) if request.form.get("restaurant_id") else None
    restaurant_check = check_restaurant(restaurant_id)
    if restaurant_check:
        return restaurant_check
    restaurant = Restaurant.query.get(restaurant_id)
    date_str = request.form.get("date")
    date = datetime.strptime(date_str, "%d.%m.%Y %H:%M").date()
    total_reserved = db.session.query(db.func.sum(Reservation.guest_number)) \
                         .filter(Reservation.restaurant_id == restaurant_id, func.date(Reservation.date) == date) \
                         .scalar() or 0
    available_seats = restaurant.total_guest_number - total_reserved
    return jsonify({"available_seats": f"available_seats: {available_seats}"}), 200


def reservation_by_id(id):
    reservation = Reservation.query.get(id)
    if reservation:
        return jsonify({
            'id': reservation.id,
            'restaurant_id': reservation.restaurant_id,
            'restaurant_name': reservation.restaurant.name if reservation.restaurant else None,  # Nazwa restauracji
            'customer_id': reservation.customer_id,
            'reservation_name': reservation.reservation_name,
            'guest_number': reservation.guest_number,
            'allergies': reservation.allergies,
            'total_cost': reservation.total_cost,
            'reservation_status': reservation.reservation_status,
            'date': reservation.date.strftime("%d.%m.%Y %H:%M")
        }), 200
    else:
        return jsonify({'error': 'Reservation not found'}), 404


def reservation_by_customer(customer_id):
    reservations = Reservation.query.filter_by(customer_id=customer_id).all()
    if reservations:
        return jsonify([{
            'id': res.id,
            'restaurant_id': res.restaurant_id,
            'restaurant_name': res.restaurant.name if res.restaurant else None,
            'customer_id': res.customer_id,
            'reservation_name': res.reservation_name,
            'guest_number': res.guest_number,
            'allergies': res.allergies,
            'total_cost': res.total_cost,
            'reservation_status': res.reservation_status,
            'date': res.date.strftime("%d.%m.%Y %H:%M")
        } for res in reservations]), 200
    else:
        return jsonify({'error': 'Reservation not found'}), 404


def reservation_by_company(company_id):
    reservations = Reservation.query.filter_by(partner_company_id=company_id).all()
    if reservations:
        return jsonify([{
            'id': res.id,
            'restaurant_id': res.restaurant_id,
            'restaurant_name': res.restaurant.name if res.restaurant else None,
            'customer_id': res.customer_id,
            'reservation_name': res.reservation_name,
            'guest_number': res.guest_number,
            'allergies': res.allergies,
            'total_cost': res.total_cost,
            'reservation_status': res.reservation_status,
            'date': res.date.strftime("%d.%m.%Y %H:%M")
        } for res in reservations]), 200
    else:
        return jsonify({'error': 'Reservation not found'}), 404


def reservation_by_date(db, date):
    if date:
        try:
            search_date = datetime.strptime(date, "%d.%m.%Y").date()
        except ValueError:
            return jsonify({'error': 'Wrong date format'}), 400

        reservations = Reservation.query.filter(db.func.date(Reservation.date) == search_date).all()
    if reservations:
        return jsonify([{
            'id': res.id,
            'restaurant_id': res.restaurant_id,
            'restaurant_name': res.restaurant.name if res.restaurant else None,
            'customer_id': res.customer_id,
            'reservation_name': res.reservation_name,
            'guest_number': res.guest_number,
            'allergies': res.allergies,
            'total_cost': res.total_cost,
            'reservation_status': res.reservation_status,
            'date': res.date.strftime("%d.%m.%Y %H:%M")
        } for res in reservations]), 200
    else:
        return jsonify({'error': 'Reservation not found'}), 404


def change_discount_customer(db):
    customer_id = request.form.get("customer_id")
    customer_check = check_customer(db, customer_id)
    if customer_check:
        return customer_check
    customer = Customer.query.get(customer_id)
    customer.discount = int(request.form.get("discount"))
    db.session.commit()
    return jsonify({
        'message': 'Customer discount was updated',
        'customer_id': customer.id,
        'new_discount': customer.discount
    }), 200


def change_discount_company(db):
    company_id = request.form.get("company_id")
    company_check = check_company(db, company_id)
    if company_check:
        return company_check
    company = PartnerCompany.query.get(company_id)
    company.discount = int(request.form.get("discount"))
    db.session.commit()
    return jsonify({
        'message': 'Partner company discount was updated',
        'customer_id': company.id,
        'new_discount': company.discount
    }), 200


def confirm_reservation(db, id):
    reservation_id = id
    cost = int(request.form.get("cost"))
    reservation = Reservation.query.get(reservation_id)
    if not reservation:
        return jsonify({'error': 'Reservation not found'}), 404
    discount = 0
    customer_id = reservation.customer_id
    if customer_id:
        customer = Customer.query.get(id)
        discount = customer.discount
    company_id = reservation.partner_company_id
    if company_id:
        company = PartnerCompany.query.get(id)
        if company.discount> discount:
            discount = company.discount
    print(cost)
    print(discount)
    reservation.total_cost = cost - cost * (discount / 100)
    reservation.reservation_status = ReservationStatus.CONFIRMED.value
    db.session.commit()
    return jsonify({
        'message': 'Reservation cost updated successfully',
        'reservation_id': reservation.id,
        'reservation_status': reservation.reservation_status,
        'new_total_cost': reservation.total_cost
    }), 200


def cancel_reservation(db, id):
    reservation_id = id
    reservation = Reservation.query.get(reservation_id)
    if not reservation:
        return jsonify({'error': 'Reservation not found'}), 404
    reservation.reservation_status = ReservationStatus.CANCELLED.value
    db.session.commit()
    return jsonify({
        'message': 'Reservation status updated successfully',
        'reservation_id': reservation.id,
        'reservation_status': reservation.reservation_status,
    }), 200


def complete_reservation(db, id):
    reservation_id = id
    reservation = Reservation.query.get(reservation_id)
    if not reservation:
        return jsonify({'error': 'Reservation not found'}), 404
    reservation.reservation_status = ReservationStatus.COMPLETED.value
    db.session.commit()
    return jsonify({
        'message': 'Reservation status updated successfully',
        'reservation_id': reservation.id,
        'reservation_status': reservation.reservation_status,
    }), 200
