"""
Tests for comment endpoints.
"""
import pytest


class TestCreateComment:
    """Tests for creating comments."""
    
    def test_create_comment_success(self, client, sample_comment_data):
        """Test successful comment creation."""
        response = client.post("/comments/", json=sample_comment_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["text"] == sample_comment_data["text"]
        assert data["owner_id"] == sample_comment_data["owner_id"]
        assert data["post_id"] == sample_comment_data["post_id"]
        assert "id" in data
        assert "created_at" in data
    
    def test_create_comment_with_votes(self, client, create_test_user, create_test_post):
        """Test creating comment with upvotes and downvotes."""
        comment_data = {
            "text": "Great post!",
            "upvotes": 5,
            "downvotes": 1,
            "owner_id": create_test_user["id"],
            "post_id": create_test_post["id"]
        }
        response = client.post("/comments/", json=comment_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["upvotes"] == 5
        assert data["downvotes"] == 1
    
    def test_create_comment_invalid_user(self, client, create_test_post):
        """Test creating comment with non-existent user fails."""
        comment_data = {
            "text": "Test comment",
            "owner_id": 999,
            "post_id": create_test_post["id"]
        }
        response = client.post("/comments/", json=comment_data)
        
        assert response.status_code == 404
        assert "User" in response.json()["detail"]
    
    def test_create_comment_invalid_post(self, client, create_test_user):
        """Test creating comment with non-existent post fails."""
        comment_data = {
            "text": "Test comment",
            "owner_id": create_test_user["id"],
            "post_id": 999
        }
        response = client.post("/comments/", json=comment_data)
        
        assert response.status_code == 404
        assert "Post" in response.json()["detail"]
    
    def test_create_comment_missing_required_fields(self, client):
        """Test creating comment without required fields fails."""
        incomplete_comment = {
            "text": "Test comment"
            # Missing owner_id and post_id
        }
        response = client.post("/comments/", json=incomplete_comment)
        
        assert response.status_code == 422  # Validation error


class TestGetComments:
    """Tests for getting comments."""
    
    def test_get_all_comments_empty(self, client):
        """Test getting comments when database is empty."""
        response = client.get("/comments/")
        
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_all_comments(self, client, sample_comment_data):
        """Test getting all comments."""
        # Create a comment
        client.post("/comments/", json=sample_comment_data)
        
        response = client.get("/comments/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["text"] == sample_comment_data["text"]
    
    def test_get_comment_by_id(self, client, sample_comment_data):
        """Test getting a specific comment by ID."""
        # Create a comment
        create_response = client.post("/comments/", json=sample_comment_data)
        comment_id = create_response.json()["id"]
        
        response = client.get(f"/comments/{comment_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == comment_id
        assert data["text"] == sample_comment_data["text"]
    
    def test_get_comment_not_found(self, client):
        """Test getting a non-existent comment."""
        response = client.get("/comments/999")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_get_comments_by_post(self, client, create_test_user, create_test_post):
        """Test getting all comments for a specific post."""
        post_id = create_test_post["id"]
        
        # Create multiple comments for the post
        for i in range(3):
            comment_data = {
                "text": f"Comment {i}",
                "owner_id": create_test_user["id"],
                "post_id": post_id
            }
            client.post("/comments/", json=comment_data)
        
        response = client.get(f"/comments/post/{post_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert all(comment["post_id"] == post_id for comment in data)
    
    def test_get_comments_by_nonexistent_post(self, client):
        """Test getting comments for a non-existent post."""
        response = client.get("/comments/post/999")
        
        assert response.status_code == 404
        assert "Post" in response.json()["detail"]
    
    def test_get_comments_by_post_empty(self, client, create_test_post):
        """Test getting comments for a post that has no comments."""
        post_id = create_test_post["id"]
        
        response = client.get(f"/comments/post/{post_id}")
        
        assert response.status_code == 200
        assert response.json() == []


class TestUpdateComment:
    """Tests for updating comments."""
    
    def test_update_comment_success(self, client, sample_comment_data):
        """Test successful comment update."""
        # Create a comment
        create_response = client.post("/comments/", json=sample_comment_data)
        comment_id = create_response.json()["id"]
        
        update_data = {
            "text": "Updated comment text",
            "upvotes": 10,
            "downvotes": 2
        }
        
        response = client.put(f"/comments/{comment_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["text"] == update_data["text"]
        assert data["upvotes"] == update_data["upvotes"]
        assert data["downvotes"] == update_data["downvotes"]
    
    def test_update_comment_not_found(self, client):
        """Test updating a non-existent comment."""
        update_data = {
            "text": "Updated text",
            "upvotes": 0,
            "downvotes": 0
        }
        
        response = client.put("/comments/999", json=update_data)
        
        assert response.status_code == 404
    
    def test_update_comment_partial(self, client, sample_comment_data):
        """Test partial update of comment."""
        # Create a comment
        create_response = client.post("/comments/", json=sample_comment_data)
        comment_id = create_response.json()["id"]
        original_text = create_response.json()["text"]
        
        # Update only upvotes
        update_data = {
            "upvotes": 15
        }
        
        response = client.put(f"/comments/{comment_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["text"] == original_text  # Unchanged
        assert data["upvotes"] == 15  # Updated


class TestDeleteComment:
    """Tests for deleting comments."""
    
    def test_delete_comment_success(self, client, sample_comment_data):
        """Test successful comment deletion."""
        # Create a comment
        create_response = client.post("/comments/", json=sample_comment_data)
        comment_id = create_response.json()["id"]
        
        response = client.delete(f"/comments/{comment_id}")
        
        assert response.status_code == 204
        
        # Verify comment is deleted
        get_response = client.get(f"/comments/{comment_id}")
        assert get_response.status_code == 404
    
    def test_delete_comment_not_found(self, client):
        """Test deleting a non-existent comment."""
        response = client.delete("/comments/999")
        
        assert response.status_code == 404


class TestCommentRelationships:
    """Tests for comment relationships with users and posts."""
    
    def test_multiple_comments_same_user(self, client, create_test_user, create_test_post):
        """Test that one user can create multiple comments."""
        user_id = create_test_user["id"]
        post_id = create_test_post["id"]
        
        # Create multiple comments from same user
        for i in range(3):
            comment_data = {
                "text": f"Comment {i}",
                "owner_id": user_id,
                "post_id": post_id
            }
            response = client.post("/comments/", json=comment_data)
            assert response.status_code == 201
        
        # Get all comments
        response = client.get("/comments/")
        data = response.json()
        
        assert len(data) == 3
        assert all(comment["owner_id"] == user_id for comment in data)
    
    def test_multiple_comments_different_posts(self, client, create_test_user):
        """Test creating comments on different posts."""
        user_id = create_test_user["id"]
        
        # Create multiple posts
        post_ids = []
        for i in range(2):
            post_data = {
                "title": f"Post {i}",
                "content": f"Content {i}",
                "owner_id": user_id
            }
            post_response = client.post("/posts/", json=post_data)
            post_ids.append(post_response.json()["id"])
        
        # Create comments on different posts
        for post_id in post_ids:
            comment_data = {
                "text": f"Comment on post {post_id}",
                "owner_id": user_id,
                "post_id": post_id
            }
            response = client.post("/comments/", json=comment_data)
            assert response.status_code == 201
        
        # Verify each post has one comment
        for post_id in post_ids:
            response = client.get(f"/comments/post/{post_id}")
            data = response.json()
            assert len(data) == 1
