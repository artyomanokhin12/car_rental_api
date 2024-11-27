from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
	
	private_key: Path = BASE_DIR / 'certs' / 'jwt-private.pem'
	public_key: Path = BASE_DIR / 'certs' / 'jwt-public.pem'


class Settings(BaseSettings):

	DB_HOST: str
	DB_PORT: int
	DB_USER: str
	DB_PASS: str
	DB_NAME: str

	@property
	def DATABASE_URL(self):
		return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

	REDIS_HOST: str
	REDIS_PORT: str

	AUTH_JWT: AuthJWT = AuthJWT()


	class Config:
		env_file = '.env'

settings = Settings()
