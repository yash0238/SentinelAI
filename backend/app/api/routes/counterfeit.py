"""
Route: Counterfeit Currency Identifier.

Endpoints (planned)
-------------------
POST /counterfeit/verify   -> accepts an image of a banknote (mobile/POS
                             capture), returns authenticity score + which
                             security features passed/failed (microprint,
                             security thread, serial-number pattern).

Powered by a Vision Transformer (google/vit-base-patch16-224) via the
HuggingFace image-classification pipeline. For the hackathon, a small curated
set of genuine vs. fake note images demonstrates the flow.

TODO
----
[ ] Define APIRouter(prefix="/counterfeit", tags=["Counterfeit"]).
[ ] Validate/resize uploaded image.
[ ] Call vision_service.classify(image) and map to feature checklist.
"""
