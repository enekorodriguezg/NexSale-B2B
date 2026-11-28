from pydantic import BaseModel

### --------------------------------------------------###

class BackupResult(BaseModel):
    file: str
    exit_code: int