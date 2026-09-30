import base64
import json
from urllib.request import urlopen

from src.legal_crop_service import InfraiClient, MatterIntake, prepare_delivery


def main() -> None:
    with urlopen("https://httpbin.org/image/jpeg", timeout=30) as response:
        image = {"base64": base64.b64encode(response.read()).decode("ascii")}
    matter = MatterIntake("matter-204", image, "signed_document")
    result = prepare_delivery(matter, InfraiClient())
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
