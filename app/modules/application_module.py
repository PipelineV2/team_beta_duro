from typing import Callable

from fastapi import FastAPI


def mount(app: FastAPI) -> Callable:
    async def start_app() -> None:
        from app.routes import home_page
        from app.routes.platform import requester_route as platform_requester_route
        # from app.routes.requester import user_route as requester_user_route
        # from app.routes.requester import auth_route as requester_auth_route
        
        

        app.include_router( home_page.router )
        app.include_router( platform_requester_route.router )
        # app.include_router( requester_user_route.router )
        # app.include_router( requester_auth_route.router )

    return start_app
