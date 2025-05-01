from flask import Flask, jsonify
from db import get_connection
from flask import request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/movies")
def get_movies():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT film_id, title, description FROM film LIMIT 10")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)

@app.route('/rent', methods=['POST'])
def rent_movie():
    data = request.get_json()
    film_id = data.get('film_id')
    customer_id = data.get('customer_id')

    if not film_id or not customer_id:
        return jsonify({'error': 'film_id and customer_id are required'}), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Verificar si el cliente ya tiene una copia activa de esa película (sin devolver)
        cursor.execute("""
            SELECT r.rental_id
            FROM rental r
            JOIN inventory i ON r.inventory_id = i.inventory_id
            WHERE r.customer_id = %s AND i.film_id = %s AND r.return_date IS NULL
        """, (customer_id, film_id))
        active_rental = cursor.fetchone()

        if active_rental:
            return jsonify({'error': 'Customer already rented this movie and has not returned it'}), 400

        # Buscar una copia disponible que no esté rentada actualmente
        cursor.execute("""
            SELECT i.inventory_id, i.store_id
            FROM inventory i
            LEFT JOIN rental r ON i.inventory_id = r.inventory_id AND r.return_date IS NULL
            WHERE i.film_id = %s AND r.inventory_id IS NULL
            LIMIT 1
        """, (film_id,))
        inventory = cursor.fetchone()

        if not inventory:
            return jsonify({'error': 'No inventory available for this film'}), 404

        inventory_id = inventory['inventory_id']
        store_id = inventory['store_id']

        # Buscar un staff_id de la tienda correspondiente
        cursor.execute("""
            SELECT staff_id FROM staff
            WHERE store_id = %s
            LIMIT 1
        """, (store_id,))
        staff = cursor.fetchone()

        if not staff:
            return jsonify({'error': 'No staff available for this store'}), 404

        staff_id = staff['staff_id']

        # Insertar la renta
        cursor.execute("""
            INSERT INTO rental (rental_date, inventory_id, customer_id, staff_id)
            VALUES (NOW(), %s, %s, %s)
        """, (inventory_id, customer_id, staff_id))

        conn.commit()
        return jsonify({
            'message': 'Movie rented successfully!',
            'customer_id': customer_id,
            'film_id': film_id,
            'inventory_id': inventory_id
        }), 201

    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()



   

@app.route('/customers', methods=['GET'])
def get_customers():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            SELECT customer_id, first_name, last_name
            FROM customer
            ORDER BY first_name
        """)
        customers = cursor.fetchall()
        return jsonify(customers)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()

@app.route('/available_movies', methods=['POST'])
def available_movies():
    data = request.get_json()
    store_id = data.get('store_id')

    if not store_id:
        return jsonify({'error': 'store_id is required'}), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT f.film_id, f.title, f.description
        FROM film f
        JOIN inventory i ON f.film_id = i.film_id
        LEFT JOIN rental r ON i.inventory_id = r.inventory_id
        WHERE i.store_id = %s
        GROUP BY f.film_id
        HAVING SUM(r.return_date IS NULL) < COUNT(*)  -- hay al menos una copia devuelta
    """, (store_id,))

    movies = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(movies)


@app.route('/return', methods=['POST'])
def return_movie():
    data = request.get_json()
    film_id = data.get('film_id')
    customer_id = data.get('customer_id')
    store_id = data.get('store_id')

    if not film_id or not customer_id:
        return jsonify({'error': 'film_id and customer_id are required'}), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Buscar la renta activa (sin return_date)
        cursor.execute("""
            SELECT r.rental_id
            FROM rental r
            JOIN inventory i ON r.inventory_id = i.inventory_id
            WHERE i.film_id = %s
              AND i.store_id = %s
              AND r.customer_id = %s
              AND r.return_date IS NULL
            LIMIT 1
        """, (film_id, store_id, customer_id))

        rental = cursor.fetchone()

        if not rental:
            return jsonify({'error': 'No active rental found for this customer and film'}), 404

        # Actualizar la renta y marcar como devuelta
        cursor.execute("""
            UPDATE rental
            SET return_date = NOW()
            WHERE rental_id = %s
        """, (rental['rental_id'],))

        conn.commit()
        return jsonify({'message': 'Movie returned successfully!'}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()



@app.route('/rented_movies', methods=['POST'])
def get_rented_movies():
    data = request.get_json()
    customer_id = data.get('customer_id')
    store_id = data.get('store_id')

    if not customer_id or not store_id:
        return jsonify({'error': 'customer_id and store_id are required'}), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT DISTINCT f.film_id, f.title, f.description
            FROM rental r
            JOIN inventory i ON r.inventory_id = i.inventory_id
            JOIN film f ON i.film_id = f.film_id
            WHERE r.customer_id = %s
              AND i.store_id = %s
              AND r.return_date IS NULL
        """, (customer_id, store_id))

        rented = cursor.fetchall()
        return jsonify(rented)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


