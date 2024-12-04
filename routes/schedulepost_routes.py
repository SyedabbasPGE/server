from flask import Blueprint, jsonify, request
from controllers.schedulepost import upload_media_to_cloudinary, save_post
from models.schedulepost import ScheduledPost

schedulepost_bp = Blueprint("schedulepost", __name__)

# Define schedule post routes
schedulepost_bp.route("/upload-media", methods=["POST"])(upload_media_to_cloudinary)
schedulepost_bp.route("/save-post", methods=["POST"])(save_post)

# Fetch all scheduled posts
@schedulepost_bp.route("/get-posts", methods=["GET"])
def get_posts():
    try:
        posts = ScheduledPost.get_scheduled_posts()
        # Convert ObjectId to string for JSON serialization
        for post in posts:
            post["_id"] = str(post["_id"])
        return jsonify(posts), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update a scheduled post
@schedulepost_bp.route("/update-post/<string:post_id>", methods=["PUT"])
def update_post(post_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No update data provided"}), 400

        updated_count = ScheduledPost.update_post(post_id, data)
        if updated_count:
            return jsonify({"message": "Post updated successfully"}), 200
        return jsonify({"error": "Post not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete a scheduled post
@schedulepost_bp.route("/delete-post/<string:post_id>", methods=["DELETE"])
def delete_post(post_id):
    try:
        deleted_count = ScheduledPost.delete_post(post_id)
        if deleted_count:
            return jsonify({"message": "Post deleted successfully"}), 200
        return jsonify({"error": "Post not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
