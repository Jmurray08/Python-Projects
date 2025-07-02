import psycopg
from datetime import datetime, date 

def get_connection():
    return psycopg.connect(
        dbname="postgres",
        user="postgres",
        password="BrodyAussie2020",
        host="localhost",
        port=5432
    )

def parse_time_input (time_str):
    try:
        return datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        return datetime.strptime(time_str, "%I:%M %p").time()

with get_connection() as conn:
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Shift (
                shift_id SERIAL PRIMARY KEY,
                date DATE NOT NULL,
                shift_type TEXT NOT NULL,
                in_time TIME NOT NULL,
                out_time TIME NOT NULL 
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS Weather (
                weather_id SERIAL PRIMARY KEY,
                shift_id INT REFERENCES Shift(shift_id) ON DELETE CASCADE,
                low_temp INT,
                high_temp INT,
                condition TEXT
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS Tips (
                tip_id SERIAL PRIMARY KEY,
                shift_id INT REFERENCES Shift(shift_id) ON DELETE CASCADE,
                amount INT NOT NULL,
                spent NUMERIC (4, 2) NOT NULL
            );
        """)


def log_shift():

    date_input = input("Enter shift date (YYYY-MM-DD): ")
    shift_type = input("Enter shift type (AM, PM, OR DOUBLE): ")
    in_time_input = input("Enter clock-in time: ")
    out_time_input = input("Enter clock-out time: ")

    shift_date = date.fromisoformat(date_input)
    in_time = parse_time_input(in_time_input)
    out_time = parse_time_input(out_time_input)

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO Shift (date, shift_type, in_time, out_time)
                VALUES (%s, %s, %s, %s)
                RETURNING shift_id;
            """, (shift_date, shift_type, in_time, out_time))

            shift_id = cur.fetchone()[0]
            print(f"\n Shift added with ID: {shift_id}!")

            low_temp = int(input("Enter low temperature of the day: "))
            high_temp = int(input("Enter high temperature of the day: "))
            conditions = input("Enter weather conditions (Sunny, Rainy, Cloudy): ")

            cur.execute("""
                INSERT INTO Weather (shift_id, low_temp, high_temp, condition)
                VALUES (%s, %s, %s, %s);
            """, (shift_id, low_temp, high_temp, conditions))
            print("Weather recorded!")

            amount = int(input("Enter the amount of tips you walked home with: "))
            spent = float(input("Enter amount spent on food/apparel/drinks(IF ANY): "))

            cur.execute("""
                INSERT INTO Tips(shift_id, amount, spent)
                VALUES (%s, %s, %s);
            """, (shift_id, amount, spent))
            print("Tip amounts recorded!")

def menu():
    print("=== TipInn Tracker ===\n")
    while True:
        print("Options:")
        print("1. Add a new shift")
        print("2. Exit")
        choice = input("Choose an option (1 or 2): ").strip()

        if choice == "1":
            log_shift()
        elif choice == "2":
            print("Thank you for your entries!")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.\n")

if __name__ == "__main__":
    menu()



    




                    





