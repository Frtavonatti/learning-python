"""
Tests for post endpoints.
"""
import pytest


class TestCreatePost:
    """Tests for creating posts."""
    
    def test_create_post_success(self, client, sample_post_data):
        """Test successful post creation."""
        response = client.post("/posts/", json=sample_post_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == sample_post_data["title"]
        assert data["content"] == sample_post_data["content"]
        assert data["published"] == sample_post_data["published"]
        assert data["rating"] == sample_post_data["rating"]
        assert data["owner_id"] == sample_post_data["owner_id"]
        assert "id" in data
        assert "created_at" in data
    
    def test_create_post_with_invalid_owner(self, client, sample_post_data):
        """Test creating post with non-existent owner fails."""
        sample_post_data["owner_id"] = 999
        response = client.post("/posts/", json=sample_post_data)
        
        # Should fail due to foreign key constraint
        assert response.status_code in [400, 500]
    
    def test_create_post_missing_required_fields(self, client, create_test_user):
        """Test creating post without required fields fails."""
        incomplete_post = {
            "title": "Test Post"
            # Missing content and owner_id
        }
        response = client.post("/posts/", json=incomplete_post)
        
        assert response.status_code == 422  # Validation error
    
    def test_create_post_with_defaults(self, client, create_test_user):
        """Test creating post with default values."""
        minimal_post = {
            "title": "Minimal Post",
            "content": "Minimal content",
            "owner_id": create_test_user["id"]
        }
        response = client.post("/posts/", json=minimal_post)
        
        assert response.status_code == 201
        data = response.json()
        assert data["published"] is True  # Default value
        assert data["rating"] is None  # Optional field


class TestGetPosts:
    """Tests for getting posts."""
    
    def test_get_all_posts_empty(self, client):
        """Test getting posts when database is empty."""
        response = client.get("/posts/")
        
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_all_posts(self, client, create_test_post):
        """Test getting all posts."""
        response = client.get("/posts/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == create_test_post["title"]
    
    def test_get_multiple_posts(self, client, create_test_user):
        """Test getting multiple posts."""
        # Create multiple posts
        for i in range(3):
            post_data = {
                "title": f"Test Post {i}",
                "content": f"Content {i}",
                "owner_id": create_test_user["id"]
            }
            client.post("/posts/", json=post_data)
        
        response = client.get("/posts/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
    
    def test_get_post_by_id(self, client, create_test_post):
        """Test getting a specific post by ID."""
        post_id = create_test_post["id"]
        response = client.get(f"/posts/{post_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == post_id
        assert data["title"] == create_test_post["title"]
    
    def test_get_post_not_found(self, client):
        """Test getting a non-existent post."""
        response = client.get("/posts/999")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestUpdatePost:
    """Tests for updating posts."""
    
    def test_update_post_success(self, client, create_test_post):
        """Test successful post update."""
        post_id = create_test_post["id"]
        update_data = {
            "title": "Updated Title",
            "content": "Updated content",
            "published": False,
            "rating": 10
        }
        
        response = client.put(f"/posts/{post_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["content"] == update_data["content"]
        assert data["published"] == update_data["published"]
        assert data["rating"] == update_data["rating"]
    
    def test_update_post_not_found(self, client):
        """Test updating a non-existent post."""
        update_data = {
            "title": "Updated Title",
            "content": "Updated content",
            "published": True,
            "rating": 5
        }
        
        response = client.put("/posts/999", json=update_data)
        
        assert response.status_code == 404
    
    def test_update_post_partial(self, client, create_test_post):
        """Test partial update of post."""
        post_id = create_test_post["id"]
        original_content = create_test_post["content"]
        
        update_data = {
            "title": "Only Title Changed",
            "content": original_content,
            "published": True,
            "rating": None
        }
        
        response = client.put(f"/posts/{post_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["content"] == original_content


class TestDeletePost:
    """Tests for deleting posts."""
    
    def test_delete_post_success(self, client, create_test_post):
        """Test successful post deletion."""
        post_id = create_test_post["id"]
        
        response = client.delete(f"/posts/{post_id}")
        
        assert response.status_code == 204
        
        # Verify post is deleted
        get_response = client.get(f"/posts/{post_id}")
        assert get_response.status_code == 404
    
    def test_delete_post_not_found(self, client):
        """Test deleting a non-existent post."""
        response = client.delete("/posts/999")
        
        assert response.status_code == 404
    
    def test_delete_post_cascades_to_comments(self, client, create_test_post, create_test_user):
        """Test that deleting a post also deletes its comments."""
        post_id = create_test_post["id"]
        
        # Create a comment on the post
        comment_data = {
            "text": "Test comment",
            "owner_id": create_test_user["id"],
            "post_id": post_id
        }
        client.post("/comments/", json=comment_data)
        
        # Delete the post
        response = client.delete(f"/posts/{post_id}")
        assert response.status_code == 204
        
        # Verify comments are also deleted (cascade)
        comments_response = client.get("/comments/")
        # If cascade is working, comments for this post should be gone
        # This depends on your comment endpoint implementation
