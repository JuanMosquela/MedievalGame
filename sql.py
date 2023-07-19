import sqlite3


def create_table():
    with sqlite3.connect("./database/medieval_adventure.db") as conexion:
        try:
            sentence = ''' CREATE TABLE IF NOT EXISTS players
                    (
                        id INTEGER primary key autoincrement,
                        username TEXT,
                        points INTEGER
                    )
                '''

            conexion.execute(sentence)

        except sqlite3.OperationalError as error:
            print(f"Error : {error}")


def save_data(username, points):
    try:
        connect = sqlite3.connect("./database/medieval_adventure.db")
        cursor = connect.cursor()
        cursor.execute(
            "INSERT INTO players (username, points) VALUES (?,?)", (username, points))
        connect.commit()
        connect.close()

    except sqlite3.OperationalError as error:
        print("Error ", error)


def load_scores():
    with sqlite3.connect("./database/medieval_adventure.db") as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM players ORDER BY points DESC")
        rows = cursor.fetchall()
        return rows
