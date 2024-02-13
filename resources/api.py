from fastapi import FastAPI, APIRouter
from controllers.order_controller import order_router
from resources.middleware import add_process_time_header
from resources.event_handler import shutdown_event, startup_event


api_router = APIRouter()
api_router.include_router(order_router, tags=["Order"],prefix="/order")

app = FastAPI(
    title="Basic ecomm app",
    contact={
        "email" : "aryantpratapsingh@gmail.com"
    }
)

app.include_router(api_router)

app.middleware("http")(add_process_time_header)



app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)