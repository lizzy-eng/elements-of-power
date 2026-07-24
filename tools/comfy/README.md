# The Owned Generative Motion Lane (ComfyUI on Lizzy's M4) — built 2026-07-24

TRUE generative motion (water flows, fire swirls, hair moves) produced entirely on
Lizzy's own hardware with open source engines. No accounts, no SaaS, no cost.

- Engine: ComfyUI (cloned from GitHub; Lizzy's fork: github.com/lizzy-eng/ComfyUI),
  installed at ~/ComfyUI with python3.12 venv, torch 2.13, Apple Metal GPU (MPS).
- Model: LTX-Video 2B v0.9.5 (models/checkpoints) + T5-XXL fp8 (models/text_encoders).
- Server: ./.venv/bin/python main.py --listen 127.0.0.1 --port 8188 (headless).
- Driver: ~/ComfyUI/eop_animate.py — full REST automation (upload frame, queue the
  LTX img2vid graph, poll, fetch clip, faststart mp4). W/H/L via env. ~3.5 min per
  2s clip at 704x448x49f on the M4.
- Batch: ~/ComfyUI/eop_batch.sh — per-element motion prompts for the 9 Ora frames.
- Proof: clip_02 (Ora awakening) 68% pixel motion start to end, character consistent,
  fire vortex swirls, water column streams. Verified by frame extraction + eye.
- Copies of both scripts live in this repo under tools/comfy/ (source of truth).
- GPU REQUIRED: this lane runs on the M4 because GitHub free runners have no GPU
  (proven infeasible: nbmd-agent-network fuckups/FUCKUP_2026-07-23_ltx-cpu-runner-infeasible.md).
