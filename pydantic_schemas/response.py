from pydantic.generics import GenericModel
from typing import Generic, Optional, TypeVar

T=TypeVar('T')

class Response(GenericModel, Generic[T]):
	code: int
	status: str
	message: str
	result : Optional[T]


	class Config:
		orm_mode=True

		
