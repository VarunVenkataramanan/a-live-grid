import base64
import io

from fastapi import HTTPException, UploadFile, status
from PIL import Image

from app.backend.core.config import settings


class LocalStorageService:
	"""Local Storage Service for image uploads"""

	def __init__(self):
		self._initialize_storage()

	def _initialize_storage(self):
		"""Initialize local storage"""
		try:
			# Create upload directory if it doesn't exist
			os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
			print("✅ Local storage initialized successfully")

		except Exception as e:
			print(f"❌ Error initializing local storage: {e}")

	def is_connected(self) -> bool:
		"""Check if storage is connected"""
		return True  # Local storage is always available

	async def upload_image(self, image_file: UploadFile, folder: str = "posts") -> str | None:
		"""
		Convert uploaded image to bitmap format
		Returns the base64 encoded bitmap string
		"""
		return await self._convert_to_bitmap(image_file)

	async def upload_base64_image(self, base64_data: str, folder: str = "posts") -> str | None:
		"""
		Convert base64 encoded image to bitmap format
		Returns the base64 encoded bitmap string
		"""
		return await self._convert_base64_to_bitmap(base64_data)

	async def delete_image(self, image_url: str) -> bool:
		"""
		Delete image (no-op for bitmap storage since images are stored as strings)
		"""
		# Since images are stored as base64 strings, there's nothing to delete
		return True

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





	async def _convert_to_bitmap(self, image_file: UploadFile) -> str:
		"""Convert uploaded image to bitmap format (base64 encoded)"""
		try:
			# Read image data
			image_data = await image_file.read()
			
			# Optimize image
			optimized_image_data = await self._optimize_image(image_data, image_file.content_type)
			
			# Convert to base64
			base64_encoded = base64.b64encode(optimized_image_data).decode('utf-8')
			
			# Return as data URL
			content_type = image_file.content_type or "image/jpeg"
			return f"data:{content_type};base64,{base64_encoded}"

		except Exception as e:
			print(f"Error converting image to bitmap: {e}")
			# Return a placeholder image as fallback
			return "data:image/jpeg;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="

	async def _convert_base64_to_bitmap(self, base64_data: str) -> str:
		"""Convert base64 encoded image to optimized bitmap format"""
		try:
			# Parse base64 data
			if base64_data.startswith("data:image/"):
				header, encoded = base64_data.split(",", 1)
				content_type = header.split(":")[1].split(";")[0]
			else:
				encoded = base64_data
				content_type = "image/jpeg"

			# Decode base64
			image_data = base64.b64decode(encoded)
			
			# Optimize image
			optimized_image_data = await self._optimize_image(image_data, content_type)
			
			# Convert back to base64
			base64_encoded = base64.b64encode(optimized_image_data).decode('utf-8')
			
			# Return as data URL
			return f"data:{content_type};base64,{base64_encoded}"

		except Exception as e:
			print(f"Error converting base64 to bitmap: {e}")
			# Return the original base64 data as fallback
			return base64_data


# Global storage service instance
storage_service = LocalStorageService()
