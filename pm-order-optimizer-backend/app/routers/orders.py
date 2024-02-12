from fastapi import APIRouter, HTTPException
from ..schemas.order_schemas import SeedOrdersInput, CreateOrderSchema, GroupOrdersInput, OrderSchema
from ..services.geodata import generate_points
from ..repositories import order_repository
from ..services.kmeanslocation import cluster_with_kmeans, cluster_with_constrained_kmeans
from geopy.geocoders import Nominatim
import geopy
from typing import List
import certifi
import ssl
from sqlalchemy.orm import Session
from fastapi import Depends
from ..dependencies import get_db

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx

router = APIRouter()
# Used http because of the ssl error
nominantim = Nominatim(user_agent="pm-order", scheme="http")


@router.post("/seed")
def seed_orders(seed_orders_input: SeedOrdersInput, db: Session = Depends(get_db)) -> List[OrderSchema]:
    points = generate_points(seed_orders_input.count)
    orders = []
    for p in points:
        order_schema = CreateOrderSchema(lat=p.y, lon=p.x)
        order = order_repository.create_order(db, order_schema)
        orders.append(order)

    return orders


@router.get("/")
def get_orders(db: Session = Depends(get_db)) -> List[OrderSchema]:
    return order_repository.get_orders(db)


@router.post("/group")
def group_orders(group_orders_input: GroupOrdersInput, db: Session = Depends(get_db)) -> List[OrderSchema]:
    orders = get_orders(db)
    if group_orders_input.algorithm == "kmeans":
        grouped_points = cluster_with_kmeans(orders, group_orders_input.group_count)
    elif group_orders_input.algorithm == "kmeans-constrained":
        grouped_points = cluster_with_constrained_kmeans(orders, group_orders_input.group_count)
    else:
        raise HTTPException(status_code=400, detail="Invalid Algorithm")
    for n in range(len(orders)):
        order_group = grouped_points[n]
        order = orders[n]
        order.group = order_group.group
        order_repository.update_group(db, order.group, order.id)

    return orders


@router.post("/reverse-geocode")
def reverse_geocode(db: Session = Depends(get_db)) -> None:
    orders = get_orders(db)
    for order in orders:
        location = nominantim.reverse((order.lat, order.lon), timeout=5)
        order_repository.update_address(db, location, order.id)


@router.delete("")
def delete_order(db: Session = Depends(get_db)) -> None:
    return order_repository.delete_orders(db)
