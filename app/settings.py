from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
	
	private_key: Path = BASE_DIR / 'certs' / 'jwt-private.pem'
	public_key: Path = BASE_DIR / 'certs' / 'jwt-public.pem'
	algorithm: str = 'RS256'
	access_token_expire_minutes: int = 15
	refresh_token_expire_days: int = 30


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

	SMTP_HOST: str
	SMTP_PORT: str
	SMTP_USER: str
	SMTP_PASS: str

	AUTH_JWT: AuthJWT = AuthJWT()

	class Config:
		env_file = '.env'

settings = Settings()


if __name__ == '__main__':
	print(settings.SMTP_HOST)
	print(settings.SMTP_PORT)