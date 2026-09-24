from pydantic import BaseModel, Field


class WeatherReport(BaseModel):
    city: str = Field(description="城市名")
    temperature: float = Field(description="摄氏温度")