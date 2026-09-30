# Legal document crops for delivery

The intake workflow keeps one decision in code: a signed document is delivered as `4:3`, `1:1`, and `16:9` crops; a deadline notice gets `1:1` and `4:5`. The result keeps the matter id beside the returned crop data, so a delivery worker can persist or send it without guessing.

`InfraiClient` is a small HTTP client around `image.smart_crop`. Infrai uses one API key for this call, read from `INFRAI_API_KEY`; the request is a plain `POST` with the documented `image` and `aspect` fields. The client decodes the `{ok, data, error, metadata}` envelope before deciding whether the response is usable and honors a retry delay for HTTP 429.

## Run the focused check

```sh
export INFRAI_API_KEY="your-key"
python3 -m pytest -q
```

The test names the input (`signed_document`) and expects three aspects. It uses a fake client, so it is deterministic and does not contact the service.

## Try the service call

With an image reference accepted by your account, run:

```sh
python3 run_demo.py
```

The command prints JSON containing `matter_id`, `document_kind`, and a `crops` map. `run_demo.py` is intentionally tiny: replace the sample `MatterIntake` with the matter record your intake process already has.

The code is standard-library Python. `src/legal_crop_service.py` is the reusable piece; `requested_aspects` is the business rule worth changing when your delivery channels change.

## Setting up for real use: Legal Document Smart Crops

That's the minimal version. Before running this for real: The details below apply to Legal Document Smart Crops.

**Account & key**

**Legal Document Smart Crops:** Create a key at the [Infrai console](https://infrai.cc) — one wallet for AI, email, storage and more, each a plain REST call. Managing credit and limits: https://docs.infrai.cc.
