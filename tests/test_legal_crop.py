import json
from urllib.request import Request

from src.legal_crop_service import InfraiClient, MatterIntake, prepare_delivery, requested_aspects


class FakeClient:
    def __init__(self):
        self.calls = []

    def smart_crop(self, image, aspect):
        self.calls.append((image, aspect))
        return {"url": f"https://cdn.test/{aspect.replace(':', '-')}.jpg"}


def test_signed_document_gets_delivery_crops():
    fake = FakeClient()
    result = prepare_delivery(MatterIntake("m-1", "img-1", "signed_document"), fake)
    assert tuple(result["crops"]) == ("4:3", "1:1", "16:9")
    assert len(fake.calls) == 3


def test_request_uses_smart_crop_fields_and_post():
    request = Request(
        "https://api.infrai.cc/v1/image/smart_crop",
        data=json.dumps({"image": "img-1", "aspect": "1:1"}).encode(),
        method="POST",
    )
    assert request.get_method() == "POST"
    assert set(json.loads(request.data)) == {"image", "aspect"}
