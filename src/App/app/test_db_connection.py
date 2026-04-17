"""Test database connection and table creation"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import SessionLocal, init_db, engine
from sqlalchemy import text

def test_connection():
    """Test database connection"""
    print("Testing database connection...")

    try:
        # Test basic connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✓ Database connection successful")

        # Initialize database tables
        print("\nInitializing database tables...")
        init_db()
        print("✓ Database tables created/verified")

        # Test session
        print("\nTesting database session...")
        db = SessionLocal()
        try:
            result = db.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result]
            print(f"✓ Available tables: {', '.join(tables)}")

            # Check if files table exists
            if 'files' in tables:
                result = db.execute(text("DESCRIBE files"))
                columns = [(row[0], row[1]) for row in result]
                print("\n✓ Files table structure:")
                for col_name, col_type in columns:
                    print(f"  - {col_name}: {col_type}")
            else:
                print("✗ 'files' table not found!")

        finally:
            db.close()

        print("\n✓ All database tests passed!")
        return True

    except Exception as e:
        print(f"\n✗ Database test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    test_connection()

