"""
Seed script to populate the dev database with sample data.

Usage:
    python -m scripts.seed
    python -m scripts.seed --clear   # clears existing data before seeding
"""
import sys
import argparse

sys.path.append(".")

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment
from scripts.data import USERS, POSTS, COMMENTS


# ---------------------------------------------------------------------------
# Seeder functions
# ---------------------------------------------------------------------------

def clear_data(db) -> None:
    print("Clearing existing data...")
    db.query(Comment).delete()
    db.query(Post).delete()
    db.query(User).delete()
    db.commit()
    print("  Done.")


def seed_users(db) -> dict[str, User]:
    print("Seeding users...")
    user_map: dict[str, User] = {}
    for data in USERS:
        existing = db.query(User).filter(User.email == data["email"]).first()
        if existing:
            print(f"  Skipping existing user: {data['username']}")
            user_map[data["username"]] = existing
            continue
        user = User(
            email=data["email"],
            username=data["username"],
            hashed_password=hash_password(data["password"]),
            roles=data["roles"],
        )
        db.add(user)
        db.flush()  # get user.id without committing
        user_map[data["username"]] = user
        print(f"  Created user: {data['username']} ({', '.join(data['roles'])})")
    db.commit()
    return user_map


def seed_posts(db, user_map: dict[str, User]) -> list[Post]:
    print("Seeding posts...")
    post_list: list[Post] = []
    for data in POSTS:
        owner = user_map[data["owner_username"]]
        post = Post(
            title=data["title"],
            content=data["content"],
            published=data["published"],
            rating=data["rating"],
            owner_id=owner.id,
        )
        db.add(post)
        db.flush()
        post_list.append(post)
        status = "published" if data["published"] else "draft"
        print(f"  Created post [{status}]: {data['title']}")
    db.commit()
    return post_list


def seed_comments(db, user_map: dict[str, User], post_list: list[Post]) -> None:
    print("Seeding comments...")
    for data in COMMENTS:
        owner = user_map[data["owner_username"]]
        post = post_list[data["post_index"]]
        comment = Comment(
            text=data["text"],
            upvotes=data["upvotes"],
            downvotes=data["downvotes"],
            owner_id=owner.id,
            post_id=post.id,
        )
        db.add(comment)
        print(f"  Created comment by {data['owner_username']} on post {data['post_index']}")
    db.commit()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Seed the dev database.")
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Clear all existing data before seeding.",
    )
    args = parser.parse_args()

    db = SessionLocal()
    try:
        if args.clear:
            clear_data(db)

        user_map = seed_users(db)
        post_list = seed_posts(db, user_map)
        seed_comments(db, user_map, post_list)

        print("\nSeeding complete!")
        print(f"  Users   : {len(user_map)}")
        print(f"  Posts   : {len(post_list)}")
        print(f"  Comments: {len(COMMENTS)}")
    except Exception as exc:
        db.rollback()
        print(f"\nError during seeding: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
