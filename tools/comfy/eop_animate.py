#!/usr/bin/env python3
"""
EOP ANIMATE — drives a local headless ComfyUI (127.0.0.1:8188) entirely via its REST
API to turn Elements of Power still frames into TRUE generative motion clips
(LTX-Video 2B on Apple Metal). No clicks, no UI, no account. Built 2026-07-23 on
Lizzy's direct order: the system does the job itself.

Usage:
  ./.venv/bin/python eop_animate.py <frame.png> <out.mp4> ["motion prompt"]

Pipeline per frame: upload image -> queue LTX img2vid workflow -> poll history ->
fetch the output video -> save. Fails loud with the server's own error if the graph
is rejected.
"""
import json, sys, time, uuid, urllib.request, urllib.error, os

HOST = "http://127.0.0.1:8188"
CKPT = "ltx-video-2b-v0.9.5.safetensors"
T5 = "t5xxl_fp8_e4m3fn_scaled.safetensors"

NEG = ("worst quality, inconsistent motion, blurry, jittery, distorted, watermark, "
       "text, letters, morphing face")


def api(path, data=None, method=None):
    req = urllib.request.Request(HOST + path, data=data, method=method or ("POST" if data else "GET"))
    if data and not isinstance(data, bytes):
        req.data = json.dumps(data).encode()
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def upload(path):
    name = os.path.basename(path)
    boundary = "EOPB0UNDARY"
    body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"image\"; filename=\"{name}\"\r\n"
            f"Content-Type: image/png\r\n\r\n").encode() + open(path, "rb").read() + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(HOST + "/upload/image", data=body, method="POST",
                                 headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read())["name"]


def workflow(image_name, prompt, width=int(os.environ.get("W",768)), height=int(os.environ.get("H",512)), length=int(os.environ.get("L",97)), fps=24, seed=770210):
    """LTX-Video img2vid graph in ComfyUI API format (per official ltxv example):
    checkpoint -> t5 clip -> text encodes -> LTXVImgToVideo latent -> LTXVConditioning
    -> SamplerCustom(euler + LTXVScheduler) -> VAEDecode -> SaveWEBM."""
    return {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": CKPT}},
        "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": T5, "type": "ltxv", "device": "default"}},
        "3": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": prompt}},
        "4": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": NEG}},
        "5": {"class_type": "LoadImage", "inputs": {"image": image_name}},
        "6": {"class_type": "LTXVImgToVideo", "inputs": {
            "positive": ["3", 0], "negative": ["4", 0], "vae": ["1", 2], "image": ["5", 0],
            "width": width, "height": height, "length": length, "batch_size": 1,
            "strength": 1.0, "crop": "disabled"}},
        "7": {"class_type": "LTXVConditioning", "inputs": {
            "positive": ["6", 0], "negative": ["6", 1], "frame_rate": float(fps)}},
        "8": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "euler"}},
        "9": {"class_type": "LTXVScheduler", "inputs": {
            "steps": 24, "max_shift": 2.05, "base_shift": 0.95, "stretch": True,
            "terminal": 0.1, "latent": ["6", 2]}},
        "10": {"class_type": "RandomNoise", "inputs": {"noise_seed": seed}},
        "11": {"class_type": "CFGGuider", "inputs": {
            "model": ["1", 0], "positive": ["7", 0], "negative": ["7", 1], "cfg": 3.0}},
        "12": {"class_type": "SamplerCustomAdvanced", "inputs": {
            "noise": ["10", 0], "guider": ["11", 0], "sampler": ["8", 0],
            "sigmas": ["9", 0], "latent_image": ["6", 2]}},
        "13": {"class_type": "VAEDecode", "inputs": {"samples": ["12", 0], "vae": ["1", 2]}},
        "14": {"class_type": "SaveWEBM", "inputs": {
            "images": ["13", 0], "filename_prefix": "eop_motion", "codec": "vp9",
            "fps": float(fps), "crf": 24.0}},
    }


def main():
    frame, out = sys.argv[1], sys.argv[2]
    prompt = sys.argv[3] if len(sys.argv) > 3 else (
        "cinematic motion, the woman breathes softly, her hair and clothing move in a gentle wind, "
        "elemental energy flows and swirls around her, fire flickers, water flows and ripples, "
        "light rays drift, slow camera push in, smooth natural movement, high quality")
    name = upload(frame)
    print("uploaded:", name)
    cid = uuid.uuid4().hex
    try:
        r = api("/prompt", {"prompt": workflow(name, prompt), "client_id": cid})
    except urllib.error.HTTPError as e:
        print("SERVER REJECTED GRAPH:\n", e.read().decode()[:3000])
        sys.exit(1)
    pid = r["prompt_id"]
    print("queued:", pid)
    t0 = time.time()
    while True:
        time.sleep(10)
        h = api(f"/history/{pid}")
        if pid in h:
            entry = h[pid]
            status = entry.get("status", {})
            if status.get("status_str") == "error":
                print("EXECUTION ERROR:\n", json.dumps(status, indent=2)[:3000])
                sys.exit(1)
            outs = entry.get("outputs", {})
            vids = []
            for node in outs.values():
                for key in ("images", "gifs", "video", "videos"):
                    for item in node.get(key, []):
                        if str(item.get("filename", "")).endswith((".webm", ".mp4")):
                            vids.append(item)
            if vids:
                v = vids[0]
                q = urllib.parse.urlencode({"filename": v["filename"], "subfolder": v.get("subfolder", ""), "type": v.get("type", "output")})
                data = urllib.request.urlopen(f"{HOST}/view?{q}", timeout=600).read()
                tmp = out + ".webm"
                open(tmp, "wb").write(data)
                os.system(f'ffmpeg -y -loglevel error -i "{tmp}" -c:v libx264 -pix_fmt yuv420p -movflags +faststart "{out}" && rm "{tmp}"')
                print(f"DONE {out} in {time.time()-t0:.0f}s")
                return
        print(f"... generating ({time.time()-t0:.0f}s)")


if __name__ == "__main__":
    import urllib.parse
    main()
