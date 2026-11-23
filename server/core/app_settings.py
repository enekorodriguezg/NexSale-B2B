import configparser
import os
import threading
from pathlib import Path

### --------------------------------------------------###

SETTINGS_FILE = Path(os.getenv("SETTINGS_FILE_PATH", "config/settings.ini"))

DEFAULT_SETTINGS = {
    "company": {
        "name": "NexSale B2B d.o.o",
        "currency": "EUR",
    },
    "inventory": {
        "low_stock_threshold": "10",
    }
}

class AppSettings:

    def __init__(self, path: Path):
        self.path = path
        self._config = configparser.ConfigParser()
        self._lock = threading.Lock()
        self.load()

    def load(self) -> None:
        with self._lock:
            self._config.read_dict(DEFAULT_SETTINGS)
            if self.path.exists():
                self._config.read(self.path, encoding = "UTF-8")
            else:
                self._save_to_file()

    def _save_to_file(self) -> None:
        self.path.parent.mkdir(parents = True, exist_ok = True)
        with open(self.path, "w", encoding = "UTF-8") as file:
            self._config.write(file)

    @property
    def company_name(self) -> str:
        return self._config.get("company", "name")
    @property
    def currency(self) -> str:
        return self._config.get("company", "currency")

    @property
    def low_stock_threshold(self) -> int:
        return self._config.getint("inventory", "low_stock_threshold")

    def update(self, company_name: str | None = None, currency: str | None = None, low_stock_threshold: int | None = None) -> None:
        with self._lock:
            if company_name is not None:
                self._config.set("company", "name", company_name)

            if currency is not None:
                self._config.set("company", "currency", currency)

            if low_stock_threshold is not None:
                self._config.set("inventory", "low_stock_threshold", str(low_stock_threshold))

            self._save_to_file()


app_settings = AppSettings(SETTINGS_FILE)


    

