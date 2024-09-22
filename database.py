import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("tic_tac_toe.db")
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute(
    """CREATE TABLE IF NOT EXISTS game_state (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     game_id INTEGER,
                     board_state TEXT NOT NULL,
                     current_player TEXT NOT NULL,
                     move_number INTEGER NOT NULL,
                     FOREIGN KEY (game_id) REFERENCES game_result(game_id))"""
)

cursor.execute(
    """CREATE TABLE IF NOT EXISTS game_result (
                     game_id INTEGER PRIMARY KEY AUTOINCREMENT,
                     winner TEXT,
                     date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"""
)


# Create a new game and get the game_id
def create_new_game():
    cursor.execute(
        """INSERT INTO game_result (winner) VALUES (NULL)"""
    )  # Insert a new game with no winner yet
    conn.commit()
    return cursor.lastrowid  # Get the ID of the newly created game


# Save the current board state
def save_game_state(game_id, board, current_player, move_number):
    board_state = "".join(board)  # Convert board list to a string
    cursor.execute(
        """INSERT INTO game_state (game_id, board_state, current_player, move_number)
                      VALUES (?, ?, ?, ?)""",
        (game_id, board_state, current_player, move_number),
    )
    conn.commit()


# Update the game result when the game is over
def save_game_result(game_id, winner):
    cursor.execute(
        """UPDATE game_result SET winner = ? WHERE game_id = ?""", (winner, game_id)
    )
    conn.commit()


# Retrieve the full game history (optional)
def retrieve_game_history(game_id):
    cursor.execute("""SELECT * FROM game_state WHERE game_id = ?""", (game_id,))
    return cursor.fetchall()


# Close the database connection
def close_connection():
    conn.close()
