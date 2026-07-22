# Elements of Power

v1.0.0. The complete engine for the Elements of Power YouTube channel: five element
series (earth, water, fire, air, spirit) taught from REAL sourced studies, rendered on
the free cloud stack (Fish Audio voice, Workers AI flux art, Remotion on lme-render
public Actions), funneling into the Activate the Elements 30 day challenge, the
ELEMENTS AND POWER journal, and declaration merch on Etsy.

- `specs/` render specs (one per episode; earth/water/fire Part 1 + channel trailer)
- `assets/` Lizzy's Canva art (design DAHQD5zZ3TY) + the LOCKED logo (seed DAHQED8Ig_4)
- `knowledge/ELEMENTS-KNOWLEDGE-BASE.md` every sourced fact with citation + care notes
- `skill/SKILL.md` the elements-of-power skill (install to ~/.claude/skills/)
- `agents/README.md` the 8 role team
- `plan/CHANNEL-PLAN.md` identity, series map, challenge, calendar, publishing SOP

Render lane lives in `lizzy-eng/lme-render`: `remotion/elements.py`,
`remotion/src/ElementsShort.tsx`, `.github/workflows/render-elements.yml`
(repository_dispatch `render-elements`). Renders land PRIVATE in Drive
"Elements of Power - Renders". Nothing posts publicly without Lizzy's word.

Install the skill on any machine:
```
git clone https://github.com/lizzy-eng/elements-of-power ~/elements-of-power 2>/dev/null || git -C ~/elements-of-power pull
mkdir -p ~/.claude/skills/elements-of-power && cp ~/elements-of-power/skill/SKILL.md ~/.claude/skills/elements-of-power/
```
