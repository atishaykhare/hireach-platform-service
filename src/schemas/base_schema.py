from pydantic import BaseModel, model_validator, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        extra='ignore', from_attributes=True)

    @model_validator(mode="before")
    def convert_objectid_to_str(self):
        if hasattr(self, 'id'):
            self.id = str(self.id)
        return self


class BasePaginationRequestSchema(BaseModel):
    query: str
    page: int = 1
    results_per_page: int
    sort_by: str = ""
    filters: dict = {}


class BasePaginationResponseSchema(BaseModel):
    total_results: int
    results: list
    page: int
    results_per_page: int
    filters: dict
    sort_by: str
