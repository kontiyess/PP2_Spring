import csv
from connect import get_connection

def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        phone VARCHAR(20)
    );
    """)

    conn.commit()
    cur.close()
    conn.close()


def insert_from_csv(filename):
    conn = get_connection()
    cur = conn.cursor()

    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            cur.execute(
                "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
                (row[0], row[1])
            )

    conn.commit()
    cur.close()
    conn.close()


def insert_manual(name, phone):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()


def update_contact(name, new_phone):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE phonebook SET phone=%s WHERE name=%s",
        (new_phone, name)
    )

    conn.commit()
    cur.close()
    conn.close()


def query_contacts():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM phonebook")
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def delete_contact(name):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM phonebook WHERE name=%s", (name,))

    conn.commit()
    cur.close()
    conn.close()


# 🚀 запуск
if __name__ == "__main__":
    create_table()

    print("1 - Insert CSV")
    print("2 - Insert manual")
    print("3 - Update")
    print("4 - Show all")
    print("5 - Delete")

    choice = input("Choose: ")

    if choice == "1":
        insert_from_csv("contacts.csv")
    elif choice == "2":
        name = input("Name: ")
        phone = input("Phone: ")
        insert_manual(name, phone)
    elif choice == "3":
        name = input("Name: ")
        phone = input("New phone: ")
        update_contact(name, phone)
    elif choice == "4":
        query_contacts()
    elif choice == "5":
        name = input("Name to delete: ")
        delete_contact(name)