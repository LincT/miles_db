import sqlite3

db_url = 'mileage.db'   # Assumes the table miles have already been created.


def add_miles(vehicle, new_miles):
    """
    If the vehicle is in the database, increment the number of miles by new_miles
    If the vehicle is not in the database, add the vehicle and set the number of miles to new_miles
    If the vehicle is None or new_miles is not a positive number, raise Error
    """
    vehicle = format_input(vehicle)

    new_miles = float(new_miles)
    if not vehicle:
        raise Exception('Provide a vehicle name ')
    if not (isinstance(new_miles, float) and new_miles >= 0):
        raise Exception('Provide a positive number for new miles ')

    conn = sqlite3.connect(db_url)
    cursor = conn.cursor()
    rows_mod = cursor.execute('UPDATE MILES SET total_miles = total_miles + ? WHERE vehicle = ?', (new_miles, vehicle))
    if rows_mod.rowcount == 0:
        cursor.execute('INSERT INTO MILES VALUES (?, ?)', (vehicle, new_miles))
    conn.commit()
    conn.close()


def format_input(input_string):
    return str(input_string).upper()


def validate_number(val_string):

    # it should fail for anything that is not a float
    # and if converting to float would raise an exception then we know it's not a valid float in string form

    try:
        if val_string.isnumeric():
            return True
        else:
            # inspiration from here: https://stackoverflow.com/a/21583824
            # using similar logic we can convert the string to a float and back to see if they still match
            return val_string == str(float(val_string))
    except ValueError:
        return False


def main():
    while True:
        vehicle = format_input(input('Enter vehicle name or enter to quit '))
        if not vehicle:
            break
        miles = (input('Enter new miles for {} '.format(vehicle)))  # TODO input validation
        if validate_float(miles) or miles.isnumeric():  # need to fix for decimals
            add_miles(vehicle, float(miles))
        else:
            print("values must be positive numbers only")
            continue


if __name__ == '__main__':
    main()
