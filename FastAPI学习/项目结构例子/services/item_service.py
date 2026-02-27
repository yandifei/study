"""物品业务逻辑服务"""

from typing import List, Optional
from sqlalchemy.orm import Session
from models.item import Item
from schemas.item import ItemCreate, ItemUpdate

class ItemService:
    """物品服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_item(self, item_id: int) -> Optional[Item]:
        """根据ID获取物品"""
        return self.db.query(Item).filter(Item.id == item_id).first()
    
    def get_items(self, skip: int = 0, limit: int = 100) -> List[Item]:
        """获取物品列表"""
        return self.db.query(Item).offset(skip).limit(limit).all()
    
    def create_item(self, item: ItemCreate, owner_id: int = 1) -> Item:
        """创建新物品"""
        db_item = Item(**item.model_dump(), owner_id=owner_id)
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item
    
    def update_item(self, item_id: int, item_update: ItemUpdate) -> Optional[Item]:
        """更新物品信息"""
        db_item = self.get_item(item_id)
        if not db_item:
            return None
        
        update_data = item_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)
        
        self.db.commit()
        self.db.refresh(db_item)
        return db_item
    
    def delete_item(self, item_id: int) -> bool:
        """删除物品"""
        db_item = self.get_item(item_id)
        if not db_item:
            return False
        
        self.db.delete(db_item)
        self.db.commit()
        return True