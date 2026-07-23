---

> DOCTRINE (Lizzy, 2026-07-23, non-negotiable): There are FOUR elements: Earth, Water, Fire, Air. Spirit is NOT an element and is never to be called one. Spirit is the SOURCE, the one who gives every element its power and made everything come alive. Spirit content honors the Source ABOVE the elements.

name: elements-of-power
description: Produce Elements of Power channel content end to end on the FREE stack. Use whenever Lizzy says "make an Elements short about X", "Elements of Power", "element short", "activate the elements", or drops studies for the channel. Covers the whole pipeline: sourced fact from the knowledge base or Studies intake folder, script in brand voice, Fish Audio narration, style locked visuals, lme-render cloud render, QA gates, PRIVATE Drive delivery, and the merch/journal funnel. Never rebuild any of this; it exists.
---

# ELEMENTS OF POWER — the channel engine (built 2026-07-21, never rebuild)

Channel: Elements of Power (handle @ElementsAndPower, name/handle final call is Lizzy's).
Teaches the four elements (earth, water, fire, air), with Spirit honored as the Source above them with REAL sourced studies.
Feel: EDUCATIONAL + MYSTICAL + SCI FI + EMPOWERING. Funnel: short -> Activate the
Elements challenge -> 30 day journal -> mug/tee on Etsy.

## Source of truth
- GitHub `lizzy-eng/elements-of-power`: specs/, assets/ (Lizzy's Canva art + locked logo),
  knowledge/ELEMENTS-KNOWLEDGE-BASE.md (sourced facts, the only place facts come from),
  agents/ (team briefs), plan/CHANNEL-PLAN.md.
- Render farm: `lizzy-eng/lme-render` (free public Actions): `remotion/elements.py` +
  `ElementsShort` composition (9:16) + `.github/workflows/render-elements.yml`
  (repository_dispatch type `render-elements`).
- Drive: folder "Elements of Power" (15MGg57yPMwWqmcwGISM3EP8jwZs2ORfM) with
  "- Studies" intake (1kLdt5UbCrfscvYiLJIQcZ8d--ER_KNbs) and "- Renders"
  (15rtdjt48OwraG95ipRBgva_XLstCiMVP, PRIVATE renders land here).

## STYLE LOCK (Production Standards Law 2, Lizzy approved once)
Locked identity: the Elements heroine emblem (assets/logo_banner.png, logo_avatar.png),
cosmic circle, water left, fire right, deep navy #10131c, cream #fef2f4, rose #c45670.
Every generation prompt carries the LOOK prefix from the specs. Openers are Lizzy's own
Canva pages (assets/opener_*.png, design DAHQD5zZ3TY), one per element per episode.

## To make a short about element X
1. FACT: take the next unused SOLID fact for X from knowledge/ELEMENTS-KNOWLEDGE-BASE.md.
   If none, read every new file in the Studies intake folder, extract + verify + append
   first. NEVER invent a fact or a citation. Respect HANDLE WITH CARE phrasing.
2. SPEC: copy specs/earth-part1.json as template. 4 scenes: opener (hook + element +
   part number, Lizzy's Canva image), teach (the fact, 45 to 70 spoken words, citation in
   ref), declare (short declaration, first person), cta (challenge day action + follow to
   next element). BRAND LAWS: no dashes as punctuation, never "free" (gift), never
   "cancel" (stop), never "transformation" (evolve). 20 to 40 seconds total narration.
3. COMMIT the spec to elements-of-power/specs/ and push (raw URL must resolve).
4. DISPATCH the render (creds from ~/.claude/projects/-Users-lizzym/memory/secrets.env;
   drive token minted from GOOGLE_REFRESH_TOKEN_DRIVE):
   POST https://api.github.com/repos/lizzy-eng/lme-render/dispatches
   {"event_type":"render-elements","client_payload":{
     "spec_url":"https://raw.githubusercontent.com/lizzy-eng/elements-of-power/main/specs/<spec>.json",
     "out_name":"NBM_ElementsPower_<Element>_Part<N>_<YYYY-MM-DD>",
     "cf_account":"<CLOUDFLARE_ACCOUNT_ID>","cf_key":"<CLOUDFLARE_MASTER_KEY>",
     "cf_email":"lizzy@youragilelady.com","fish_key":"<FISH_API_KEY>",
     "drive_token":"<minted access token>","folder":"15rtdjt48OwraG95ipRBgva_XLstCiMVP"}}
5. The workflow enforces Laws 1 to 4 (Fish voice first + fail loud, style lock, max 7s
   holds, audio transcribe back QA, vision QA per image, final duration/stream/frame QA)
   and uploads the MP4 PRIVATE to the Renders folder. Watch the run to completion; on
   fail, read the log, fix, redispatch.
6. VERIFY like a human: download the artifact frames (or Drive MP4), LOOK at them,
   confirm narration matches visuals. Report the real Drive link.
7. PUBLISH GATE (Law 10): nothing posts to YouTube without Lizzy's word per piece.
   Buy links go under a video ONLY after the Etsy listing is verified live and
   purchasable. Real live link or no link.

## Merch + journal
Printify shop 28175574 -> Etsy. Declarations become mug + tee designs (locked identity).
Journal: "ELEMENTS AND POWER, A 30 Day Activation Journal" (Drive PDF + PRINT_SPEC.md).
Publish to Etsy ONLY after Lizzy confirms design + price; then verify the live listing
loads and is purchasable before any buy link is used anywhere.

## The team (agents/README.md)
Element Researcher, Short Scripter, Voice, Visualist, Assembler, QA, Merch, Publisher.
Run them as roles of this skill; each brief is in agents/README.md in the repo.
