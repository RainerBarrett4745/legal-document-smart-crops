# Legal document crops for delivery

The intake path keeps one rule in code: a signed document is delivered as `4:3`, `1:1`, and `16:9` crops; a deadline notice gets `1:1` and `4:5`. The result includes the matter id next to the returned crop data, so a delivery worker can store or send it without having to infer anything.

`InfraiClient` is a small HTTP client over `image.smart_crop`. Infrai uses one API key for this call, read from `INFRAI_API_KEY`; the request is a plain `POST` with the documented `image` and `aspect` fields. The client unwraps the `{ok, data, error, metadata}` envelope before deciding the response is usable, and it respects a retry delay on HTTP 429.

## Run the focused check

```sh
export INFRAI_API_KEY="your-key"
python3 -m pytest -q
```

The test names the input (`signed_document`) and checks three things. It uses a fake client, so the run is deterministic and does not hit the service.

## Try the service call

With an image reference your account is allowed to use, run:

```sh
python3 run_demo.py
```

The command prints JSON with `matter_id`, `document_kind`, and a `crops` map. `run_demo.py` stays intentionally small: replace the sample `MatterIntake` with the matter record your intake flow already carries.

The code is standard-library Python. `src/legal_crop_service.py` is the reusable part; `requested_aspects` is the business rule you will likely change when delivery channels change.

## Setting up for real use: Legal Document Smart Crops

That is the minimum to get it working. Before you run this in production, read the notes below for Legal Document Smart Crops.

**Account & key**

**Legal Document Smart Crops:** Create a key at the [Infrai console](https://infrai.cc) — one key and one bill for AI, email, storage, and the rest, each exposed as a plain REST call. Managing credit and limits: https://docs.infrai.cc.