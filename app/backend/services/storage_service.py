import base64
import io
import os
import uuid

from fastapi import HTTPException, UploadFile, status
from google.cloud import storage
from google.cloud.exceptions import NotFound
from PIL import Image

from app.backend.core.config import settings


class GoogleCloudStorageService:
	"""Google Cloud Storage Service for image uploads"""

	def __init__(self):
		self.client = None
		self.bucket = None
		self._initialize_storage()

	def _initialize_storage(self):
		"""Initialize Google Cloud Storage client"""
		try:
			# Initialize the storage client
			self.client = storage.Client(project=settings.FIREBASE_PROJECT_ID)

			# Get the bucket
			self.bucket = self.client.bucket(settings.FIREBASE_STORAGE_BUCKET)

			print("✅ Google Cloud Storage initialized successfully")

		except Exception as e:
			print(f"❌ Error initializing Google Cloud Storage: {e}")
			self.client = None
			self.bucket = None

	def is_connected(self) -> bool:
		"""Check if storage is connected"""
		return self.client is not None and self.bucket is not None

	async def upload_image(self, image_file: UploadFile, folder: str = "posts") -> str | None:
		"""
		Upload image to Google Cloud Storage
		Returns the public URL of the uploaded image
		"""
		if not self.is_connected():
			raise HTTPException(
				status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
				detail="Storage service not available",
			)

		try:
			# Generate unique filename
			file_extension = self._get_file_extension(image_file.filename)
			filename = f"{folder}/{uuid.uuid4()}{file_extension}"

			# Read and process image
			image_data = await image_file.read()

			# Optimize image if needed
			optimized_image_data = await self._optimize_image(image_data, image_file.content_type)

			# Create blob
			blob = self.bucket.blob(filename)

			# Set content type
			blob.content_type = image_file.content_type

			# Upload image
			blob.upload_from_string(optimized_image_data, content_type=image_file.content_type)

			# Make blob publicly readable
			blob.make_public()

			# Return public URL
			return blob.public_url

		except Exception as e:
			print(f"Error uploading image: {e}")
			raise HTTPException from e(
				status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
				detail=f"Failed to upload image: {e!s}",
			)

	async def upload_base64_image(self, base64_data: str, folder: str = "posts") -> str | None:
		"""
		Upload base64 encoded image to Google Cloud Storage
		Returns the public URL of the uploaded image
		"""
		if not self.is_connected():
			raise HTTPException(
				status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
				detail="Storage service not available",
			)

		try:
			# Parse base64 data
			if base64_data.startswith("data:image/"):
				# Remove data URL prefix
				header, encoded = base64_data.split(",", 1)
				content_type = header.split(":")[1].split(";")[0]
			else:
				encoded = base64_data
				content_type = "image/jpeg"

			# Decode base64
			image_data = base64.b64decode(encoded)

			# Generate filename
			file_extension = self._get_extension_from_content_type(content_type)
			filename = f"{folder}/{uuid.uuid4()}{file_extension}"

			# Optimize image
			optimized_image_data = await self._optimize_image(image_data, content_type)

			# Create blob
			blob = self.bucket.blob(filename)
			blob.content_type = content_type

			# Upload image
			blob.upload_from_string(optimized_image_data, content_type=content_type)

			# Make blob publicly readable
			blob.make_public()

			# Return public URL
			return blob.public_url

		except Exception as e:
			print(f"Error uploading base64 image: {e}")
			raise HTTPException from e(
				status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
				detail=f"Failed to upload image: {e!s}",
			)

	async def delete_image(self, image_url: str) -> bool:
		"""
		Delete image from Google Cloud Storage
		"""
		if not self.is_connected():
			return False

		try:
			# Extract blob name from URL
			blob_name = self._extract_blob_name_from_url(image_url)

			# Get blob
			blob = self.bucket.blob(blob_name)

			# Delete blob
			blob.delete()

			return True

		except NotFound:
			# Blob doesn't exist
			return True
		except Exception as e:
			print(f"Error deleting image: {e}")
			return False

	async def _optimize_image(self, image_data: bytes, content_type: str) -> bytes:
		"""
		Optimize image for storage
		"""
		try:
			# Open image
			image = Image.open(io.BytesIO(image_data))

			# Convert to RGB if necessary
			if image.mode in ("RGBA", "LA", "P"):
				# Create white background
				background = Image.new("RGB", image.size, (255, 255, 255))
				if image.mode == "P":
					image = image.convert("RGBA")
				background.paste(image, mask=image.split()[-1] if image.mode == "RGBA" else None)
				image = background

			# Resize if too large
			max_size = (1920, 1920)
			if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
				image.thumbnail(max_size, Image.Resampling.LANCZOS)

			# Save optimized image
			output = io.BytesIO()

			if content_type == "image/png":
				image.save(output, format="PNG", optimize=True)
			elif content_type == "image/gif":
				image.save(output, format="GIF", optimize=True)
			else:
				# Default to JPEG
				image.save(output, format="JPEG", quality=85, optimize=True)

			return output.getvalue()

		except Exception as e:
			print(f"Error optimizing image: {e}")
			# Return original data if optimization fails
			return image_data

	def _get_file_extension(self, filename: str) -> str:
		"""Get file extension from filename"""
		if not filename:
			return ".jpg"

		name, ext = os.path.splitext(filename.lower())
		if ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]:
			return ext
		return ".jpg"

	def _get_extension_from_content_type(self, content_type: str) -> str:
		"""Get file extension from content type"""
		content_type_map = {
			"image/jpeg": ".jpg",
			"image/jpg": ".jpg",
			"image/png": ".png",
			"image/gif": ".gif",
			"image/webp": ".webp",
		}
		return content_type_map.get(content_type, ".jpg")

	def _extract_blob_name_from_url(self, url: str) -> str:
		"""Extract blob name from public URL"""
		try:
			# Remove base URL to get blob name
			base_url = f"https://storage.googleapis.com/{settings.FIREBASE_STORAGE_BUCKET}/"
			if url.startswith(base_url):
				return url[len(base_url) :]
			return url
		except Exception:
			return url


# Global storage service instance
storage_service = GoogleCloudStorageService()
