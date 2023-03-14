from __future__ import annotations
from typing import List, Dict, Any
from pydantic import BaseModel

class Schema(BaseModel):
	Age: float 
	RoomService: float 
	FoodCourt: float
	shoppingMall: float
	Spa: float 
	VRDeck: float 
	HomePlanet: str 
	CryoSleep: bool
	Destination: str 
	VIP: bool
	