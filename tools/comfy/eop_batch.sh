#!/bin/bash
# EOP batch: animate all remaining Ora frames sequentially on the M4 (one GPU).
cd ~/ComfyUI
P_BASE="cinematic motion, smooth natural movement, high quality, slow camera push in"
declare -a FRAMES=(01 03 04 05 06 07 08 09)
declare -A PROMPTS=(
 [01]="$P_BASE, the woman writes with her pen, candle flames flicker, the angels' robes drift softly, golden dust motes float in the light"
 [03]="$P_BASE, the woman breathes in prayer, the white dove's wings beat slowly, liquid gold and living water pour and stream from the vessels, light rays intensify"
 [04]="$P_BASE, the arc of water flows and streams like a living river, spray and droplets drift, the woman's arms guide the current, the seated people breathe"
 [05]="$P_BASE, the green light veins pulse and flow through the roots like energy, dust drifts, the woman's hair moves softly, the elders watch and breathe"
 [06]="$P_BASE, the storm clouds churn slowly, the fire spiral flickers and licks upward, the water spiral flows, her dress and hair move in the wind"
 [07]="$P_BASE, the book glows brighter and pages shimmer, flames flicker on the left, water streams on the right, glowing script letters drift through the air"
 [08]="$P_BASE, the white wind vortexes spin and curl, clouds drift past the mountain, both figures' clothes ripple in the strong wind"
 [09]="$P_BASE, the elemental swirls of fire water and wind spin around the joyful people, debris floats, hair and fabrics fly, radiant light pulses"
)
for f in "${FRAMES[@]}"; do
  echo "=== frame $f ==="
  W=704 H=448 L=49 ./.venv/bin/python eop_animate.py eop_frames/ora_$f.png eop_out/clip_$f.mp4 "${PROMPTS[$f]}" || echo "FRAME $f FAILED"
done
echo "BATCH COMPLETE: $(ls eop_out/clip_*.mp4 | wc -l) clips"
