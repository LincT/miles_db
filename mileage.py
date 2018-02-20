import sqlite3

db_url = 'mileage.db'   # Assumes the table miles have already been created.


def add_miles(vehicle, new_miles):
    """
    If the vehicle is in the database, increment the number of miles by new_miles
    If the vehicle is not in the database, add the vehicle and set the number of miles to new_miles
    If the vehicle is None or new_miles is not a positive number, raise Error
    """
    vehicle = format_input(vehicle)
    if not vehicle:
        raise Exception('Provide a vehicle name')
    if not (isinstance(new_miles, float) and new_miles >= 0):
        raise Exception('Provide a positive number for new miles')

    conn = sqlite3.connect(db_url)
    cursor = conn.cursor()
    rows_mod = cursor.execute('UPDATE MILES SET total_miles = total_miles + ? WHERE vehicle = ?', (new_miles, vehicle))
    if rows_mod.rowcount == 0:
        cursor.execute('INSERT INTO MILES VALUES (?, ?)', (vehicle, new_miles))
    conn.commit()
    conn.close()


def format_input(input_string):
    return str(input_string).upper()


def validate_number():
    pass


def main():
    while True:
        vehicle = format_input(input('Enter vehicle name or enter to quit'))
        if not vehicle:
            break
        miles = float(input('Enter new miles for %s' % vehicle))  # TODO input validation

        add_miles(vehicle, miles)


if __name__ == '__main__':
    main()
