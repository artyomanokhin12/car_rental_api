from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix='/user',
    tags=['Фронтэнд Пользователя']
)

templates = Jinja2Templates(directory="app/templates/users")


@router.get('/login')
async def get_hotels_page(
	request: Request  
):
    return templates.TemplateResponse(
        name='login.html', 
        context={"request": request}
        )
