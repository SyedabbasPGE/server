from flask import request, jsonify
from cloudinary.uploader import upload
import requests
import os
from apscheduler.schedulers.background import BackgroundScheduler
from models.schedulepost import ScheduledPost

# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.start()


def upload_media_to_cloudinary():
    """Handles media upload to Cloudinary."""
    if 'media' not in request.files:
        return jsonify({"error": "No media file provided"}), 400

    media_file = request.files['media']
    try:
        # Upload to Cloudinary
        result = upload(media_file)
        cloudinary_url = result['secure_url']
        
        # Store the URL in the database
        ScheduledPost.store_media({
            "cloudinary_url": cloudinary_url,
            "filename": os.path.basename(media_file.filename)
        })
        return jsonify({"message": "Media uploaded successfully", "url": cloudinary_url}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Save post to the database (in controllers/schedulepost.py)
def save_post():
    """Handles saving a scheduled post."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Extract post data
        post_text = data.get("postText")
        media_files = data.get("mediaFiles", [])
        post_time = data.get("postTime")
        accounts = data.get("accounts", [])  # This now contains account names

        if not accounts:
            return jsonify({"error": "No accounts selected"}), 400

        # Save post to the database
        post_id = ScheduledPost.store_post({
            "postText": post_text,
            "mediaFiles": media_files,
            "postTime": post_time,
            "accounts": accounts,  # Store account names directly
        })

        return jsonify({"message": "Post saved successfully", "post_id": post_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500



def download_media():
    """Downloads scheduled media from Cloudinary."""
    scheduled_media = ScheduledPost.get_all_scheduled_media()
    for media in scheduled_media:
        cloudinary_url = media['cloudinary_url']
        filename = media['filename']
        try:
            print(f"Downloading from: {cloudinary_url}")
            response = requests.get(cloudinary_url, stream=True)
            response.raise_for_status()

            # Ensure the test folder exists
            save_path = os.path.join('backend/test', filename)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            # Save the file
            with open(save_path, 'wb') as media_file:
                for chunk in response.iter_content(chunk_size=8192):
                    media_file.write(chunk)

            print(f"File successfully saved to: {save_path}")

            # Mark the media as downloaded
            ScheduledPost.mark_as_downloaded(media['_id'])
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {cloudinary_url}: {e}")
        except Exception as e:
            print(f"Error while processing media {media['_id']}: {e}")


# Schedule the download_media function to run every day
scheduler.add_job(download_media, 'interval', days=1)
