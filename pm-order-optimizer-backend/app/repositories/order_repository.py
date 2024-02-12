from ..models.order_models import Order
from ..schemas.order_schemas import CreateOrderSchema
from sqlalchemy.orm import Session


def get_orders(db: Session):
    return db.query(Order).all()


def get_order(db: Session, id: int) -> Order:
    return db.query(Order).filter(Order.id == id).first()


def create_order(db: Session, order: CreateOrderSchema):
    db_order = Order(
        lat=order.lat,
        lon=order.lon,
        address=order.address,
        group=order.group
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def update_address(db: Session, address: str, id: int):
    db.query(Order).filter(Order.id == id).update(
        {
            "address": address
        })
    db.commit()


def update_group(db: Session, group: int, id: int):
    db.query(Order).filter(Order.id == id).update(
        {
            "group": group
        }
    )
    db.commit()


def delete_orders(db: Session):
    db.query(Order).delete()
    db.commit()
