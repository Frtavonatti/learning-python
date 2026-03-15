"""
Clears all data from the dev database without dropping tables.

Usage:
    python -m scripts.clear_db
"""
import sys

sys.path.append(".")

from app.core.database import SessionLocal
from app.models.comment import Comment
from app.models.post import Post
from app.models.user import User


def main() -> None:
    db = SessionLocal()
    try:
        comments = db.query(Comment).delete()
        posts = db.query(Post).delete()
        users = db.query(User).delete()
        db.commit()
        print(f"Deleted: {comments} comments, {posts} posts, {users} users.")
    except Exception as exc:
        db.rollback()
        print(f"Error: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
