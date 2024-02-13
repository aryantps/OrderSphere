from db import db_manager
from uvicorn.main import logger
from utils import convert_to_dict
from db.dao.order_dao import OrderDao
from fastapi import APIRouter, Body, Depends

from schemas.order_schema import OrderSchema
from schemas.exception_schema import AppException
from schemas.response_schema import ResponseModel, PaginatedResponse
from schemas.request_schema import PaginatedRequest, SearchOrderRequest




order_router = APIRouter()

@order_router.post("/create", response_description="Order data added into the database")
async def create_order(
    order: OrderSchema = Body(...),
):
    try:
        order_dict = convert_to_dict(order)
        logger.debug(f"order_router : create_order : order_dict - {order_dict}")
        order_dao = OrderDao(db_manager)
        await order_dao.add_order(order_dict)
        return ResponseModel(data=convert_to_dict(order_dict), message="order added successfully.")
    except Exception as e:
        error_message = f"An error occurred while adding the order: {str(e)}"
        logger.error(error_message, exc_info=1)
        raise AppException(status_code=500, detail=error_message) from e

@order_router.get("/list/paginated", response_model=PaginatedResponse)
async def get_paginated_orders(request_params: PaginatedRequest = Depends()):
    try:
        logger.debug(f"order_router : get_paginated_orders : PaginatedRequest - {request_params}")
        order_dao = OrderDao(db_manager)
        return await order_dao.get_paginated_orders(
            request_params.page, request_params.limit, request_params.min_price, request_params.max_price
        )
    except Exception as e:
        error_message = f"An error occurred while getting paginated order list : {str(e)}"
        logger.error(error_message, exc_info=1)
        raise AppException(status_code=500, detail=error_message) from e
    

@order_router.get("/search")
async def search_orders(request_params: SearchOrderRequest = Depends()):
    try:
        logger.debug(f"order_router : search_orders : SearchOrderRequest - {request_params}")
        order_dao = OrderDao(db_manager)
        order_details = await order_dao.search_order(
            request_params
        )
        return ResponseModel(data=convert_to_dict(order_details), message="Order fetched successfully.")
    except Exception as e:
        error_message = f"An error occurred while searching order : {str(e)}"
        logger.error(error_message, exc_info=1)
        raise AppException(status_code=500, detail=error_message) from e
    

@order_router.get("/{order_id}")
async def get_order_by_order_id(order_id : str):
    try:
        logger.debug(f"order_router : get_order_by_order_id : order_id - {order_id}")
        order_dao = OrderDao(db_manager)
        order_details = await order_dao.search_order({
            "_id": order_id
            })
        return ResponseModel(data=convert_to_dict(order_details), message="Order fetched successfully.")
    except Exception as e:
        error_message = f"An error occurred while fetching order : {str(e)}"
        logger.error(error_message, exc_info=1)
        raise AppException(status_code=500, detail=error_message) from e