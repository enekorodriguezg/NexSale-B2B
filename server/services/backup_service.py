import sys
import subprocess
from pathlib import Path

from fastapi import HTTPException, status

from server.schemas.backup_schema import BackupResult

### --------------------------------------------------###

BACKUP_SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "backup_data.py"
BACKUP_TIMEOUT_SECONDS = 60

ERRORS_BY_EXIT_CODE = {
    1: (status.HTTP_409_CONFLICT, "There are no data files to back up"),
    2: (status.HTTP_500_INTERNAL_SERVER_ERROR, "The backup file could not be written"),
}

### --------------------------------------------------###

def create_backup() -> BackupResult:
    try:
        result =subprocess.run(
            [sys.executable, str(BACKUP_SCRIPT)],
            capture_output = True,
            text = True,
            timeout = BACKUP_TIMEOUT_SECONDS
        )

    except subprocess.TimeoutExpired as e:
        raise HTTPException(
            status_code = status.HTTP_504_GATEWAY_TIMEOUT,
            detail = "The backup process took too long and was stopped"
        ) from e

    if result.returncode != 0:
        http_status, message = ERRORS_BY_EXIT_CODE.get(
            result.returncode, (status.HTTP_500_INTERNAL_SERVER_ERROR, "The backup process failed unexpectedly")
        )

        raise HTTPException(
            status_code = http_status,
            detail = message
        )

    return BackupResult(file = result.stdout.strip(), exit_code = result.returncode)
