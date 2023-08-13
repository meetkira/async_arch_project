from typing import Optional

from sqlalchemy.orm import Session

from auth.dto.user import User
from auth import models


class CRUDUser:
    def __int__(self, model: models.User):
        self.model = model

    def get(self, db: Session, obj_id: int):
        return db.query(self.model).filter(self.model.id == obj_id).first()

    def list(self, db: Session):
        return db.query(self.model).all()

    def create(self, db: Session, *, obj_in: User):
        obj_in_data = obj_in.model_dump()
        #захешировать пароль
        db_obj = self.model(**obj_in_data)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, obj_id: int):
        obj: Optional[models.User] = db.get(self.model, obj_id)
        if obj is None:
            raise Exception(f"Model of type {self.model} with id={obj_id} not found")
        db.delete(obj)
        db.commit()

        return obj


user = CRUDUser(models.User)
