"""
Database Service
Business logic cho MongoDB operations
"""

from typing import Optional, Any
from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.utils.helpers import (
    validate_object_id,
    get_current_timestamp,
    sort_histories_by_name,
)
from .connection import get_database
from .models import (
    HistoryLevelModel,
    ImageCreateRequest,
    ImageUpdateRequest,
    HistoryCreateRequest,
    HistoryUpdateRequest,
    HistoryItemCreateRequest,
    ImportCreateRequest,
)


class DatabaseService:
    """Service xử lý các operations với MongoDB"""

    def __init__(self):
        self.db: AsyncIOMotorDatabase = get_database()
        self.images = self.db.images
        self.histories = self.db.histories
        self.imports = self.db.imports

    # ==================== IMAGES OPERATIONS ====================

    async def create_image(self, data: ImageCreateRequest) -> dict:
        """
        Tạo mới image document

        Args:
            data: ImageCreateRequest

        Returns:
            Dictionary chứa inserted_id và document
        """
        doc = data.model_dump()
        doc["created_at"] = get_current_timestamp()
        doc["updated_at"] = get_current_timestamp()

        result = await self.images.insert_one(doc)
        doc["_id"] = str(result.inserted_id)

        return doc

    async def get_image(self, image_id: str) -> Optional[dict]:
        """
        Lấy image theo ID

        Args:
            image_id: ID của image

        Returns:
            Dictionary hoặc None nếu không tìm thấy
        """
        if not validate_object_id(image_id):
            return None

        doc = await self.images.find_one({"_id": ObjectId(image_id)})
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    async def list_images(
        self,
        skip: int = 0,
        limit: int = 10,
        sort_by: str = "created_at",
        sort_order: int = -1,
    ) -> list[dict]:
        """
        Lấy danh sách images

        Args:
            skip: Số documents bỏ qua
            limit: Số documents tối đa
            sort_by: Field để sort
            sort_order: 1 (ascending) hoặc -1 (descending)

        Returns:
            List of dictionaries
        """
        cursor = self.images.find().sort(sort_by, sort_order).skip(skip).limit(limit)
        docs = await cursor.to_list(length=limit)

        for doc in docs:
            doc["_id"] = str(doc["_id"])

        return docs

    async def update_image(
        self, image_id: str, data: ImageUpdateRequest
    ) -> Optional[dict]:
        """
        Cập nhật image

        Args:
            image_id: ID của image
            data: ImageUpdateRequest

        Returns:
            Dictionary hoặc None nếu không tìm thấy
        """
        if not validate_object_id(image_id):
            return None

        # Chỉ update các field không None
        update_data = {k: v for k, v in data.model_dump().items() if v is not None}

        if not update_data:
            return await self.get_image(image_id)

        update_data["updated_at"] = get_current_timestamp()

        result = await self.images.update_one(
            {"_id": ObjectId(image_id)}, {"$set": update_data}
        )

        if result.matched_count == 0:
            return None

        return await self.get_image(image_id)

    async def delete_image(self, image_id: str) -> bool:
        """
        Xóa image

        Args:
            image_id: ID của image

        Returns:
            True nếu xóa thành công, False nếu không
        """
        if not validate_object_id(image_id):
            return False

        result = await self.images.delete_one({"_id": ObjectId(image_id)})
        return result.deleted_count > 0

    async def count_images(self, filter_query: Optional[dict] = None) -> int:
        """
        Đếm số lượng images

        Args:
            filter_query: Query filter (optional)

        Returns:
            Số lượng documents
        """
        if filter_query is None:
            filter_query = {}
        return await self.images.count_documents(filter_query)

    # ==================== HISTORIES OPERATIONS ====================

    async def create_history(self, data: HistoryCreateRequest) -> dict:
        """Tạo history record"""
        doc = data.model_dump()
        doc["timestamp"] = get_current_timestamp()

        result = await self.histories.insert_one(doc)
        doc["_id"] = str(result.inserted_id)

        return doc

    async def list_histories(
        self,
        collection: Optional[str] = None,
        document_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 10,
        sort_by: str = "updatedAt",
        sort_order: str = "desc",
        search: Optional[str] = None,
    ) -> list[dict]:
        """
        Lấy danh sách histories với sorting và search

        Args:
            collection: Filter theo collection (optional)
            document_id: Filter theo document_id (optional)
            skip: Số records bỏ qua
            limit: Số records tối đa
            sort_by: Field để sort ('name' hoặc 'updatedAt')
            sort_order: Thứ tự sort ('asc' hoặc 'desc')
            search: Tìm kiếm theo name (case-insensitive)

        Returns:
            List of history documents
        """
        query = {}
        if collection:
            query["collection"] = collection
        if document_id:
            query["document_id"] = document_id

        # Add search filter
        if search:
            # Case-insensitive regex search on value.name
            query["value.name"] = {"$regex": search, "$options": "i"}

        # Nếu sort by name hoặc có search, cần fetch tất cả rồi sort ở application level
        # vì name có thể là số dạng string ("4", "41", "51")
        if sort_by == "name" or search:
            # Fetch tất cả documents matching query
            cursor = self.histories.find(query)
            all_docs = await cursor.to_list(length=None)

            # Convert ObjectId to string
            for doc in all_docs:
                doc["_id"] = str(doc["_id"])

            # Sort by name với numeric comparison
            if sort_by == "name":
                sorted_docs = sort_histories_by_name(all_docs, sort_order)
            else:
                # Sort by updatedAt
                sorted_docs = sorted(
                    all_docs,
                    key=lambda x: x.get("updatedAt", ""),
                    reverse=(sort_order == "desc"),
                )

            # Apply pagination
            paginated_docs = sorted_docs[skip : skip + limit]

            return paginated_docs
        else:
            # Sort by updatedAt - có thể dùng MongoDB sort
            sort_direction = 1 if sort_order == "asc" else -1

            cursor = (
                self.histories.find(query)
                .sort("updatedAt", sort_direction)
                .skip(skip)
                .limit(limit)
            )
            docs = await cursor.to_list(length=limit)

            for doc in docs:
                doc["_id"] = str(doc["_id"])

            return docs

    async def get_history(self, history_id: str) -> Optional[dict]:
        """
        Lấy history theo ID

        Args:
            history_id: History ID

        Returns:
            History document hoặc None
        """
        if not validate_object_id(history_id):
            return None

        doc = await self.histories.find_one({"_id": ObjectId(history_id)})
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    async def update_history(
        self, history_id: str, data: HistoryLevelModel
    ) -> Optional[dict]:
        """
        Cập nhật history level data

        Args:
            history_id: History ID (value.id)
            data: HistoryLevelModel với level data mới

        Returns:
            Updated document hoặc None nếu không tìm thấy
        """
        current_time = get_current_timestamp()

        # Update value.level với data mới
        update_data = {
            "value.level": data.model_dump(),
            "value.updatedAt": current_time,
            "updatedAt": current_time,
        }

        result = await self.histories.find_one_and_update(
            {"value.id": history_id}, {"$set": update_data}, return_document=True
        )

        if result:
            result["_id"] = str(result["_id"])
        return result

    async def update_history_name(self, history_id: str, name: str) -> Optional[dict]:
        """
        Cập nhật tên history (value.name)

        Args:
            history_id: History ID
            name: Tên mới

        Returns:
            Updated document hoặc None nếu không tìm thấy
        """

        result = await self.histories.find_one_and_update(
            {"value.id": history_id},
            {
                "$set": {
                    "value.name": name,
                    "value.updatedAt": get_current_timestamp(),
                    "updatedAt": get_current_timestamp(),
                }
            },
            return_document=True,
        )

        if result:
            result["_id"] = str(result["_id"])
        return result

    async def delete_history(self, history_id: str) -> bool:
        """
        Xóa history

        Args:
            history_id: History ID

        Returns:
            True nếu xóa thành công, False nếu không tìm thấy
        """

        result = await self.histories.delete_one({"value.id": history_id})
        return result.deleted_count > 0

    async def create_history_item(self, data: HistoryItemCreateRequest) -> dict:
        """
        Tạo history item với auto-generation cho missing fields

        Auto-generates:
        - value.id (nếu không có)
        - value.level.id = value.id (same ID)
        - value.level.config.id = value.id (same ID)
        - value.level.config.createdAt (nếu không có)
        - value.level.config.updatedAt (nếu không có)
        - value.createdAt (nếu không có)
        - value.updatedAt (nếu không có)
        - timestamp (root level)
        """
        import uuid
        from datetime import datetime

        doc = data.model_dump()
        current_time = get_current_timestamp()

        # Auto-generate value.id (base ID cho tất cả)
        if not doc.get("value", {}).get("id"):
            doc["value"][
                "id"
            ] = f"level_{int(datetime.utcnow().timestamp() * 1000)}_{uuid.uuid4().hex[:8]}"

        # Lấy base ID
        base_id = doc["value"]["id"]

        # Set value.level.id = value.id
        if not doc.get("value", {}).get("level", {}).get("id"):
            doc["value"]["level"]["id"] = base_id

        # Set value.level.config.id = value.id
        if not doc.get("value", {}).get("level", {}).get("config", {}).get("id"):
            doc["value"]["level"]["config"]["id"] = base_id

        # Auto-generate value.level.timestamp
        if not doc.get("value", {}).get("level", {}).get("timestamp"):
            # Format với microseconds như trong data mẫu
            doc["value"]["level"]["timestamp"] = datetime.utcnow().strftime(
                "%Y-%m-%dT%H:%M:%S.%f"
            )

        # Auto-generate timestamps
        if not doc.get("value", {}).get("level", {}).get("config", {}).get("createdAt"):
            doc["value"]["level"]["config"]["createdAt"] = current_time

        if not doc.get("value", {}).get("level", {}).get("config", {}).get("updatedAt"):
            doc["value"]["level"]["config"]["updatedAt"] = current_time

        if not doc.get("value", {}).get("createdAt"):
            doc["value"]["createdAt"] = current_time

        if not doc.get("value", {}).get("updatedAt"):
            doc["value"]["updatedAt"] = current_time

        # Add root timestamp
        doc["timestamp"] = current_time

        # Insert to MongoDB
        result = await self.histories.insert_one(doc)
        doc["_id"] = str(result.inserted_id)

        return doc

    async def count_histories(
        self,
        collection: Optional[str] = None,
        document_id: Optional[str] = None,
        search: Optional[str] = None,
    ) -> int:
        """
        Đếm số lượng histories

        Args:
            collection: Filter theo collection (optional)
            document_id: Filter theo document_id (optional)
            search: Tìm kiếm theo name (optional)

        Returns:
            Số lượng documents
        """
        query = {}
        if collection:
            query["collection"] = collection
        if document_id:
            query["document_id"] = document_id
        if search:
            query["value.name"] = {"$regex": search, "$options": "i"}

        return await self.histories.count_documents(query)

    # ==================== IMPORTS OPERATIONS ====================

    async def create_import(self, data: ImportCreateRequest) -> dict:
        """Tạo import record"""
        doc = data.model_dump()
        doc["status"] = "pending"
        doc["processed_items"] = 0
        doc["failed_items"] = 0
        doc["started_at"] = get_current_timestamp()

        result = await self.imports.insert_one(doc)
        doc["_id"] = str(result.inserted_id)

        return doc

    async def get_import(self, import_id: str) -> Optional[dict]:
        """Lấy import theo ID"""
        if not validate_object_id(import_id):
            return None

        doc = await self.imports.find_one({"_id": ObjectId(import_id)})
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    async def update_import_status(
        self,
        import_id: str,
        status: str,
        processed_items: Optional[int] = None,
        failed_items: Optional[int] = None,
        error_message: Optional[str] = None,
    ) -> Optional[dict]:
        """Cập nhật trạng thái import"""
        if not validate_object_id(import_id):
            return None

        update_data = {"status": status}

        if processed_items is not None:
            update_data["processed_items"] = processed_items
        if failed_items is not None:
            update_data["failed_items"] = failed_items
        if error_message is not None:
            update_data["error_message"] = error_message

        if status in ["completed", "failed"]:
            update_data["completed_at"] = get_current_timestamp()

        await self.imports.update_one(
            {"_id": ObjectId(import_id)}, {"$set": update_data}
        )

        return await self.get_import(import_id)

    async def list_imports(self, skip: int = 0, limit: int = 10) -> list[dict]:
        """Lấy danh sách imports"""
        cursor = self.imports.find().sort("started_at", -1).skip(skip).limit(limit)
        docs = await cursor.to_list(length=limit)

        for doc in docs:
            doc["_id"] = str(doc["_id"])

        return docs


# Singleton instance
database_service = DatabaseService()
