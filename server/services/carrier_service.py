import threading
import xml.etree.ElementTree as ET

from fastapi import HTTPException, status

from server.core.config import CARRIERS_XML_FILE

### --------------------------------------------------###

_xml_lock = threading.Lock()

CHILD_FIELDS = ["name", "phone", "price_per_shipment", "delivery_days"]

### --------------------------------------------------###

def _load_root() -> ET.Element:
    if not CARRIERS_XML_FILE.exists():
        return ET.Element("carriers")
    return ET.parse(CARRIERS_XML_FILE).getroot()

def _save_root(root: ET.Element) -> None:
    CARRIERS_XML_FILE.parent.mkdir(parents = True, exist_ok = True)
    tree = ET.ElementTree(root)
    ET.indent(tree, space = "  ")
    tree.write(CARRIERS_XML_FILE, encoding = "utf-8", xml_declaration = True)

def _get_text(carrier: ET.Element, tag: str) -> str:
    text = carrier.findtext(tag)
    if text is None:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"Carriers file is corrupted: <{tag}> is missing is carrier {carrier.get("code")}"
        )
    return text

def _element_to_dict(carrier: ET.Element) -> dict:
    return{
        "code": carrier.get("code"),
        "name": _get_text(carrier = carrier, tag = "name"),
        "phone": _get_text(carrier = carrier, tag = "phone"),
        "price_per_shipment": float(_get_text(carrier = carrier, tag = "price_per_shipment")),
        "delivery_days": int(_get_text(carrier = carrier, tag = "delivery_days")),
    }

def _find_element(root: ET.Element, code: str) -> ET.Element:
    for carrier in root.findall("carrier"):
        if carrier.get("code") == code:
            return carrier
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = f"Carrier with code {code} not found"
    )

### --------------------------------------------------###

def get_carriers() -> list[dict]:
    with _xml_lock:
        root = _load_root()
    return [_element_to_dict(carrier) for carrier in root.findall("carrier")]

def create_carrier(carrier: dict) -> dict:
    with _xml_lock:
        root = _load_root()
        if any(existing.get("code") == carrier["code"] for existing in root.findall("carrier")):
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = f"Carrier with code {carrier['code']} already exists"
            )

        element = ET.SubElement(root, "carrier", code = carrier["code"])
        for field in CHILD_FIELDS:
            ET.SubElement(element, field).text = str(carrier[field])

        _save_root(root = root)
        return _element_to_dict(carrier = element)


def update_carrier(code: str, changes: dict) -> dict:
    with _xml_lock:
        root = _load_root()
        element = _find_element(root = root, code = code)
        for field, value in changes.items():
            child = element.find(field)
            if child is None:
                child = ET.SubElement(element, field)
            child.text = str(value)

        _save_root(root = root)
        return _element_to_dict(carrier = element)

def delete_carrier(code: str) -> None:
    with _xml_lock:
        root = _load_root()
        element = _find_element(root = root, code = code)
        root.remove(element)
        _save_root(root = root)

    
