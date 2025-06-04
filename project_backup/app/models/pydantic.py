from pydantic import BaseModel, AnyHttpUrl

class SummaryPayloadFromText(BaseModel):
    text: str

class SummaryFromTextResponseSchema(SummaryPayloadFromText):
    summary: str

class SummaryPayloadSchema(BaseModel):
    url: AnyHttpUrl


class SummaryResponseSchema(SummaryPayloadSchema):
    id: int


class SummaryUpdatePayloadSchema(SummaryPayloadSchema):
    summary: str
