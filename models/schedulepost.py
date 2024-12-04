from config import db
from bson import ObjectId

# MongoDB collection for scheduled posts
scheduled_posts_collection = db.scheduled_posts

class ScheduledPost:
    @staticmethod
    def store_media(media_data):
        """
        Store media metadata in the database.
        Marks the media as not downloaded yet by default.
        """
        media_data['downloaded'] = False  # Mark as not downloaded yet
        return str(scheduled_posts_collection.insert_one(media_data).inserted_id)

    @staticmethod
    def get_all_scheduled_media():
        """
        Fetch all media that have not been downloaded yet.
        """
        return list(scheduled_posts_collection.find({"downloaded": False}))

    @staticmethod
    def mark_as_downloaded(media_id):
        """
        Mark a media file as downloaded in the database.
        """
        if not isinstance(media_id, ObjectId):
            media_id = ObjectId(media_id)  # Convert to ObjectId if necessary
        scheduled_posts_collection.update_one(
            {"_id": media_id}, {"$set": {"downloaded": True}}
        )

    @staticmethod
    def store_post(post_data):
        """
        Store scheduled post details in the database.
        This includes post text, media URLs, accounts, and the scheduled time.
        """
        return str(scheduled_posts_collection.insert_one(post_data).inserted_id)

    @staticmethod
    def get_scheduled_posts():
        """
        Fetch all scheduled posts from the database.
        This can be used to list or process scheduled posts.
        """
        return list(scheduled_posts_collection.find())

    @staticmethod
    def delete_post(post_id):
        """
        Delete a specific post from the database using its ObjectId.
        """
        if not isinstance(post_id, ObjectId):
            post_id = ObjectId(post_id)  # Convert to ObjectId if necessary
        return scheduled_posts_collection.delete_one({"_id": post_id}).deleted_count

    @staticmethod
    def update_post(post_id, update_data):
        """
        Update a specific post in the database using its ObjectId.
        """
        if not isinstance(post_id, ObjectId):
            post_id = ObjectId(post_id)  # Convert to ObjectId if necessary
        return scheduled_posts_collection.update_one(
            {"_id": post_id}, {"$set": update_data}
        ).modified_count
