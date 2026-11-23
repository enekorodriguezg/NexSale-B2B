from pydantic import BaseModel, Field, field_validator


### --------------------------------------------------###

class SettingsResponse(BaseModel):
    company_name: str
    currency: str
    low_stock_threshold: int

class SettingsUpdate(BaseModel):
    company_name: str | None = Field(default = None, min_length = 1, max_length = 100)
    currency: str | None = Field(default = None, pattern = "^[A-Z]{3}$")
    low_stock_threshold: int | None = Field(default = None, ge = 0)

    @field_validator("company_name")
    @classmethod
    def validate_pdf_compatible(cls, value: str | None) -> str | None:
        if value is not None:
            try:
                value.encode("latin-1")
            except UnicodeEncodeError:
                raise ValueError("Company name can only contain Latin-1 characters (no č, ć, š, ž, đ)")
        return value
