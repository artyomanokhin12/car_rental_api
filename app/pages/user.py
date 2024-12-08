from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.users.models import Users
from app.users.router import get_current_user


router = APIRouter(
    tags=['Фронтэнд Пользователя']
)

templates = Jinja2Templates(directory="app/templates")


@router.get('/login', response_class=HTMLResponse)
async def get_hotels_page(
	request: Request  
):
    return templates.TemplateResponse(
        name='users/login.html', 
        context={"request": request}
        )


@router.get('/me', response_class=HTMLResponse)
async def get_user(
    request: Request,
    user = Depends(get_current_user)
):
    return templates.TemplateResponse(
        name='users/get_user.html',
        context={
            'request': request,
            'user': user,
		}
	)
