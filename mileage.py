import sqlite3

db_url = 'mileage.db'   # Assumes the table miles have already been created.


class MileageError(Exception):
    pass


def add_miles(vehicle, new_miles):
    """
    If the vehicle is in the database, increment the number of miles by new_miles
    If the vehicle is not in the database, add the vehicle and set the number of miles to new_miles
    If the vehicle is None or new_miles is not a positive number, raise Error
    """
    vehicle = format_input(vehicle)

    new_miles = float(new_miles)
    if not vehicle:
        raise MileageError('Provide a vehicle name ')
    if not isinstance(new_miles, (int, float)) or new_miles < 0:
        raise MileageError('Provide a positive number for new miles ')

    conn = sqlite3.connect(db_url)
    cursor = conn.cursor()
    rows_mod = cursor.execute('UPDATE MILES SET total_miles = total_miles + ? WHERE vehicle = ?', (new_miles, vehicle))
    if rows_mod.rowcount == 0:
        cursor.execute('INSERT INTO MILES VALUES (?, ?)', (vehicle, new_miles))
    conn.commit()
    conn.close()


def search_entries(parm=""):
    conn = sqlite3.connect(db_url)
    cursor = conn.cursor()
    with conn:
        if parm == "":
            result_set = cursor.execute('select * from miles').fetchall()
            results = [": ".join(str(item) for item in tuple(each)) for each in result_set]
        else:
            result_set = cursor.execute('select * from MILES where vehicle = ?', (parm,)).fetchall()
            results = [": ".join(str(item) for item in tuple(each)) for each in result_set]
    return results


def format_input(input_string):
    # this could have easily been in the main function as a one line add on,
    # but better to seperate in case future iterations want more complex formatting
    return str(input_string).upper()


def validate_number(val_string):

    # it should fail for anything that is not a number, and if converting to float
    #  would raise an exception then we know it's not a valid number in string form,
    # however we need to go deeper than .isnumber as "0.1" was coming back false

    try:
        if val_string.isnumeric():  # if it registers as numeric then we know it can be converted to numeric types
            return True
        else:
            # inspiration from here: https://stackoverflow.com/a/21583824
            # using similar logic we can convert the string to a float and back to see if they still match
            return val_string.find(str(float(val_string))) >= 0
    except ValueError:
        return False


def main():
    while True:
        vehicle = format_input(input('Enter vehicle name to add, "search" to find an entry, or enter to quit '))
        print(vehicle)
        if not vehicle:
            break
        if vehicle.lower() == "search":
            query = input("entry to search for").upper().strip()
            results = search_entries(query)
            print("\n".join(str(each) for each in results))
        else:
            miles = (input('Enter new miles for {} '.format(vehicle)))
            # input validation
            if validate_number(miles):  # if it's a valid number, we can convert to a float
                add_miles(vehicle, float(miles))
            else:
                print("values must be positive numbers only")
                continue


if __name__ == '__main__':
    main()
