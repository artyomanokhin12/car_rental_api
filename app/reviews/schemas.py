from pydantic import BaseModel, ConfigDict


class ReviewResponse(BaseModel):

	model_config = ConfigDict(extra='forbid')

	id: int
	booking_id: int
	rating: int
	commend: str | None = None
