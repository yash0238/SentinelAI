# Notebooks

Exploration and tuning notebooks. Create as needed:

- `01_audio_threshold_tuning.ipynb` — find the synthetic-voice score cut-off
  that balances precision/recall on your sample set.
- `02_zeroshot_label_experiments.ipynb` — try label wordings, measure accuracy
  on your transcript fixtures.
- `03_vision_currency_probe.ipynb` — sanity-check the ViT on genuine vs. fake
  note images.

Keep notebooks lightweight; move anything reusable into
`backend/app/services/`.
