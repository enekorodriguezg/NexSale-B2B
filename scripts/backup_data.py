"""Process B (R14): creates a compressed backup of the application data files.

It is started by the API (process A) through POST /backups, but it can also be run by hand:
    python scripts/backup_data.py

Exit codes:
    0 -> backup created (its file name is printed on stdout)
    1 -> there are no data files to back up
    2 -> the backup file could not be written
"""

import sys
from datetime import datetime
import tarfile

from server.core.config import SUPPLIERS_JSON_FILE, CARRIERS_XML_FILE, SETTINGS_FILE, BACKUPS_DIR

### --------------------------------------------------###

EXIT_OK = 0
EXIT_NOTHING_TO_BACKUP = 1
EXIT_WRITE_ERROR = 2

FILES_TO_BACKUP = [SUPPLIERS_JSON_FILE, CARRIERS_XML_FILE, SETTINGS_FILE]

### --------------------------------------------------###

def main() -> int:
    existing_files = [file for file in FILES_TO_BACKUP if file.exists()]
    if not existing_files:
        print("There are no data files to backup", file = sys.stderr)
        return EXIT_NOTHING_TO_BACKUP

    backup_file = BACKUPS_DIR / f"nexsale_backup_{datetime.now():%Y%m%d_%H%M%S}.tar.gz"
    try:
        BACKUPS_DIR.mkdir(parents = True, exist_ok = True)
        with tarfile.open(backup_file, "w:gz") as tar:
            for file in existing_files:
                tar.add(file, arcname = file.name)

    except OSError as e:
        print(f"Could not write the backup: {e}", file = sys.stderr)
        return EXIT_WRITE_ERROR

    print(backup_file.name)
    return EXIT_OK
            


if __name__ == "__main__":
    sys.exit(main())