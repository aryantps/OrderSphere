from bson.objectid import ObjectId

from db.connection import DbConnectionManager
from uvicorn.main import logger

class OrderDao:
    def __init__(self, db_manager: DbConnectionManager):
        self.db_manager = db_manager

        
    async def add_order(self, order_data: dict) -> dict:
        await self.db_manager.connect_to_database()
        collection = self.db_manager.db.get_collection("orders")
        await collection.insert_one(order_data)
        return 
        
    async def get_paginated_orders(self, page: int, limit: int, min_price: float = None, max_price: float = None):
        await self.db_manager.connect_to_database()
        collection = self.db_manager.db.get_collection("orders")
        pipeline = self.build_pagination_aggregation_pipeline(page, limit, min_price, max_price)
        logger.info(f"Starting paginated query with pipeline - {pipeline}")
        result = await collection.aggregate(pipeline).to_list(None)
        logger.info("Done paginated query...")
        return self.process_pagination_aggregation_result(result, page, limit)
    
    def build_pagination_aggregation_pipeline(self, page: int, limit: int, min_price: float = None, max_price: float = None):
        # Match stage for filtering based on price
        match_stage = {}
        if min_price is not None:
            match_stage["price"] = {"$gte": min_price}
        if max_price is not None:
            match_stage["price"] = {"$lte": max_price}

        # Pagination and filtering using aggregation pipeline
        return [
                #Stage 1: Match documents based on filtering
                {"$match": match_stage},
                #Stage 2: Perform multiple independent aggregations on the same set of input documents
                {
                    "$facet": {
                        #Sub-pipeline 1: Calculate metadata about the result set
                        "metadata": [
                            #Count the total number of documents
                            {"$count": "total"},
                            #Add pagination metadata (page and limit)
                            {"$addFields": {"page": page, "limit": limit}},
                        ],
                        #Sub-pipeline 2: Paginate the data
                        "data": [
                            #Skip a certain number of documents based on pagination parameters
                            {"$skip": (page - 1) * limit},
                            #Limit the number of documents returned per page
                            {"$limit": limit},
                        ],
                    }
                },
            ]

    def process_pagination_aggregation_result(self, result, page, limit):
        if not result:
            return {
                "page": 1,
                "limit": limit,
                "nextOffset": None,
                "prevOffset": None,
                "total": 0,
                "data": []
            }
        metadata = result[0]["metadata"][0]
        data = result[0]["data"]
        return {
            "page": metadata["page"],
            "limit": metadata["limit"],
            "nextOffset": page * limit if metadata["total"] > page * limit else None,
            "prevOffset": (page - 2) * limit if page > 1 else None,
            "total": metadata["total"],
            "data": [order_id_helper(item) for item in data]
        }
    
    async def search_order(self, filter_criteria: dict) -> dict:
        await self.db_manager.connect_to_database()
        collection = self.db_manager.db.get_collection("orders")
        filter_dict = self.generate_filter(filter_criteria=filter_criteria)

        cursor = collection.find(filter_dict)
        return [order_id_helper(order) for order in await cursor.to_list(None)]
    
    def generate_filter(self, filter_criteria: dict) -> dict:
        filter_dict = {}
        if '_id' in filter_criteria:
            filter_dict['_id'] = ObjectId(filter_criteria['_id'])

        # Add other filters based on provided criteria
        if 'productId' in filter_criteria:
            filter_dict['items.productId'] = filter_criteria['productId']

        if 'city' in filter_criteria:
            filter_dict['userAddress.city'] = filter_criteria['city']

        if 'zipCode' in filter_criteria:
            filter_dict['userAddress.zipCode'] = filter_criteria['zipCode']

        return filter_dict
        
def order_id_helper(order) -> dict:
    order["id"] = str(order.pop("_id", None))
    return order

