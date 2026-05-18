# database/score_manager.py
from database.db import get_connection
#WE USED "PARAMETERISED QUERIES" PLACE HOLDER TO AVOID SQL INJECTION THRGH AN API REQUEST THE QUERY WILL BE SAVED INSTED OF EXECUTED 
class ScoreManager:
    @staticmethod
    def save_game_result(user_id: int, word: str, difficulty: str,
                         attempts_used: int, hints_used: int,
                         won: bool, score: int, time_seconds: int = None) -> None:
        """
        Store result in the database.
        All values are provided by the game logic .

        """
        with get_connection() as conn:
            conn.execute('''
                INSERT INTO scores (user_id, word, difficulty, attempts_used,
                                    hints_used, time_seconds, won, score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, word, difficulty, attempts_used, hints_used,
                  time_seconds, won, score))
            conn.commit()

    @staticmethod
    def get_leaderboard_by_points(limit: int = 10): #I DIDN'T USE THE "APPLES TO APPLES" PRINCIPLE
        """
        Return the overall leaderboard sorted by score (points) descending.
         ranking by points.
        """
        #THE REASEN WHY WE LOADS s.difficulty, s.played_at IS TO GIVE TRANSPARITY 
        query = '''
            SELECT u.username, s.score, s.difficulty, s.played_at 
            FROM scores s
            JOIN users u ON s.user_id = u.id
            ORDER BY s.score DESC
            LIMIT ?
        '''
        with get_connection() as conn:
            rows = conn.execute(query, (limit,)).fetchall() # fetchall() create a list 
            return [dict(row) for row in rows] # PYTHON WAY TO DO THINGS

    @staticmethod
    def get_user_stats(user_id: int):
        """Return summary statistics based on stored data (can be used by GUI)."""
        with get_connection() as conn:  #Context Manager "with" automaticly closes the conction ones this block is finished 
            row = conn.execute('''
                SELECT
                    COUNT(*) as total_games,
                    SUM(CASE WHEN won = 1 THEN 1 ELSE 0 END) as wins,
                    SUM(CASE WHEN won = 0 THEN 1 ELSE 0 END) as losses,
                    SUM(hints_used) as total_hints,
                    SUM(time_seconds) as total_play_time_seconds,
                    AVG(attempts_used) as avg_attempts_per_game,
                    AVG(score) as avg_score,
                    SUM(score) as total_score
                FROM scores
                WHERE user_id = ?
            ''', (user_id,)).fetchone() # TO GROUPE ALL USER DATA TO ONE ROW
            return dict(row)
        
    @staticmethod
    def save_game_result(user_id: int, word: str, difficulty: str,
                         attempts_used: int, hints_used: int,
                         won: bool, time_seconds: int = None) -> int:
        """
        Calculate score and store the game result in the database.
        Returns the computed score.
        """
        
        base_points = {"easy": 100, "medium": 200, "hard": 300}.get(difficulty.lower(), 100)

        
        remaining_attempts = max(0, 6 - attempts_used)
        attempt_bonus = remaining_attempts * 10

        
        hint_penalty = hints_used * 15

        
        time_bonus = 0
        if time_seconds:
            if difficulty.lower() == "easy" and time_seconds < 20:
                time_bonus = 20
            elif difficulty.lower() == "medium" and time_seconds < 30:
                time_bonus = 35
            elif difficulty.lower() == "hard" and time_seconds < 40:
                time_bonus = 50

        if won:
            total_score = base_points + attempt_bonus - hint_penalty + time_bonus
            total_score = max(total_score, 10)   # minimum 10 points for a win
        else:
            total_score = 0

        # --- Store in database ---
        with get_connection() as conn:
            conn.execute('''
                INSERT INTO scores (user_id, word, difficulty, attempts_used,
                                    hints_used, time_seconds, won, score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, word, difficulty, attempts_used, hints_used,
                  time_seconds, won, total_score))
            conn.commit()

        return total_score
    
    @staticmethod
    def get_user_rankings(limit: int = 20):
        """
        Return list of dicts: {rank, username, total_score, total_games, wins}
        Ordered by total_score descending.
        """
        query = '''
            SELECT 
                u.username,
                COALESCE(SUM(s.score), 0) as total_score,
                COUNT(s.id) as total_games,
                SUM(CASE WHEN s.won = 1 THEN 1 ELSE 0 END) as wins
            FROM users u
            LEFT JOIN scores s ON u.id = s.user_id
            GROUP BY u.id, u.username
            ORDER BY total_score DESC
            LIMIT ?
        '''
        with get_connection() as conn:
            rows = conn.execute(query, (limit,)).fetchall()
            rankings = []
            for idx, row in enumerate(rows, start=1):
                rankings.append({
                    'rank': idx,
                    'username': row['username'],
                    'total_score': row['total_score'],
                    'total_games': row['total_games'],
                    'wins': row['wins']
                })
            return rankings