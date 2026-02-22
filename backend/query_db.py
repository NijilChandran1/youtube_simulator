#!/usr/bin/env python3
"""
Query script for training.db
Displays all tables and their contents in a readable format
"""

import sqlite3
from pathlib import Path
from tabulate import tabulate
from datetime import datetime

# Database path
DB_PATH = Path(__file__).parent / "data" / "training.db"

def connect_db():
    """Connect to the training database"""
    if not DB_PATH.exists():
        print(f"❌ Database not found at: {DB_PATH}")
        print("Please ensure the database has been initialized.")
        return None
    return sqlite3.connect(DB_PATH)

def query_users(conn):
    """Query and display all users"""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    
    if rows:
        headers = ["ID", "Username", "Email", "Full Name", "Created At"]
        print("\n" + "="*80)
        print("👥 USERS")
        print("="*80)
        print(tabulate(rows, headers=headers, tablefmt="grid"))
        print(f"Total: {len(rows)} user(s)")
    else:
        print("\n👥 USERS: No records found")

def query_videos(conn):
    """Query and display all videos"""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM videos")
    rows = cursor.fetchall()
    
    if rows:
        headers = ["ID", "Video ID", "Title", "File Path", "Duration (s)", "Broadcast Start", "Created At"]
        print("\n" + "="*80)
        print("📹 VIDEOS")
        print("="*80)
        print(tabulate(rows, headers=headers, tablefmt="grid"))
        print(f"Total: {len(rows)} video(s)")
    else:
        print("\n📹 VIDEOS: No records found")

def query_sessions(conn):
    """Query and display all training sessions"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            ts.id,
            ts.user_id,
            u.username,
            ts.video_id,
            ts.started_at,
            ts.completed_at,
            ts.status
        FROM training_sessions ts
        LEFT JOIN users u ON ts.user_id = u.id
    """)
    rows = cursor.fetchall()
    
    if rows:
        headers = ["Session ID", "User ID", "Username", "Video ID", "Started At", "Completed At", "Status"]
        print("\n" + "="*80)
        print("🎯 TRAINING SESSIONS")
        print("="*80)
        print(tabulate(rows, headers=headers, tablefmt="grid"))
        print(f"Total: {len(rows)} session(s)")
    else:
        print("\n🎯 TRAINING SESSIONS: No records found")

def query_ground_truth(conn):
    """Query and display all ground truth events"""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ground_truth_events where video_id='super_bowl_2026' ORDER BY timestamp_seconds")
    rows = cursor.fetchall()
    
    if rows:
        headers = ["ID", "Video ID", "Attribute", "Timestamp (s)", "Live Clock Time", "Clue Description", "Created At"]
        print("\n" + "="*80)
        print("✅ GROUND TRUTH EVENTS")
        print("="*80)
        print(tabulate(rows, headers=headers, tablefmt="grid"))
        print(f"Total: {len(rows)} event(s)")
    else:
        print("\n✅ GROUND TRUTH EVENTS: No records found")

def query_attempts(conn):
    """Query and display all user attempts"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            ua.id,
            ua.session_id,
            ua.attribute,
            ua.user_timestamp_seconds,
            ua.user_live_clock_time,
            ua.time_difference_ms,
            ua.accuracy_level,
            ua.ai_feedback,
            ua.created_at
        FROM user_attempts ua
        ORDER BY ua.created_at DESC
    """)
    rows = cursor.fetchall()
    
    if rows:
        headers = ["ID", "Session", "Attribute", "User Time (s)", "Live Clock", "Diff (ms)", "Accuracy", "AI Feedback", "Created At"]
        print("\n" + "="*80)
        print("📊 USER ATTEMPTS")
        print("="*80)
        
        # Truncate AI feedback for display
        display_rows = []
        for row in rows:
            row_list = list(row)
            if row_list[7]:  # AI feedback column
                row_list[7] = (row_list[7][:50] + '...') if len(row_list[7]) > 50 else row_list[7]
            display_rows.append(row_list)
        
        print(tabulate(display_rows, headers=headers, tablefmt="grid"))
        print(f"Total: {len(rows)} attempt(s)")
    else:
        print("\n📊 USER ATTEMPTS: No records found")

def query_session_summary(conn, session_id=None):
    """Display summary statistics for a session or all sessions"""
    cursor = conn.cursor()
    
    if session_id:
        where_clause = f"WHERE ua.session_id = {session_id}"
        title = f"SESSION {session_id} SUMMARY"
    else:
        where_clause = ""
        title = "ALL SESSIONS SUMMARY"
    
    cursor.execute(f"""
        SELECT 
            accuracy_level,
            COUNT(*) as count,
            AVG(time_difference_ms) as avg_diff_ms
        FROM user_attempts ua
        {where_clause}
        GROUP BY accuracy_level
    """)
    rows = cursor.fetchall()
    
    if rows:
        headers = ["Accuracy Level", "Count", "Avg Time Diff (ms)"]
        print("\n" + "="*80)
        print(f"📈 {title}")
        print("="*80)
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    else:
        print(f"\n📈 {title}: No attempts found")

def main():
    """Main query function"""
    print("\n" + "="*80)
    print("🗄️  EPG TRAINING DATABASE QUERY TOOL")
    print("="*80)
    print(f"Database: {DB_PATH}")
    
    conn = connect_db()
    if not conn:
        return
    
    try:
        # Query all tables
        #query_users(conn)
        #query_videos(conn)
        query_ground_truth(conn)
        #query_sessions(conn)
        #query_attempts(conn)
        #query_session_summary(conn)
        
        print("\n" + "="*80)
        print("✅ Query complete!")
        print("="*80 + "\n")
        
    except sqlite3.Error as e:
        print(f"\n❌ Database error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
