# Style recipes — say a look in one line

Pick one recipe before writing prompts. Consistency of look across clips is what separates a video from a slideshow of generations. Each recipe gives you a paste-ready style block.

## How to use

1. Pick a recipe (or blend two, never three).
2. Paste its **STYLE** line into the FORMAT block of every prompt.
3. Keep the palette and lens constant; vary only subject and beats.

---

## 1 · Cinematic narrative
```
STYLE: 2.39:1 (or 9:16 crop), shot on 35mm anamorphic, shallow depth of field,
teal shadows and warm skin tones, motivated practical light, gentle grain,
no lens flare, restrained camera.
```
Use for: story, drama, brand film. Key light from a visible source.

## 2 · Documentary handheld
```
STYLE: handheld 35mm, natural available light, slight exposure breathing,
documentary framing, no colour grade beyond a gentle contrast curve, room
tone in every shot.
```
Use for: real stories, behind-the-scenes, testimonials. Imperfection is the point.

## 3 · Product commercial
```
STYLE: 100mm macro, black or seamless gradient background, hard key from
top-right, soft rim light, controlled reflections, slow orbit or slider,
razor focus on the label, no hands unless specified.
```
Use for: product hero shots. Clean surfaces, one highlight.

## 4 · UGC / phone-native
```
STYLE: smartphone front or rear camera, vertical 9:16, slight handheld shake,
mild autofocus hunting, mixed indoor light, no stabilisation, diegetic sound
only, occasional overexposure near windows.
```
Use for: authenticity, testimonials, ads that must not look like ads.

## 5 · 3D cartoon (kids / family)
```
STYLE: bright 3D animation, soft rounded shapes, saturated but not neon,
warm sand / teal / coral palette, gentle ambient occlusion, clean uncluttered
backgrounds, oversized expressive eyes, no film grain, no photorealism.
```
Use for: children's education, mascots, explainers for families.

## 6 · Flat vector explainer
```
STYLE: 2D flat vector, limited palette of 4 colours, thick consistent strokes,
no gradients, geometric shapes, simple looping motion, generous negative space.
```
Use for: finance, SaaS, process explainers. Cheap to keep consistent.

## 7 · Paper / stop motion
```
STYLE: stop-motion paper craft, visible paper texture and cut edges, tactile
shadows, shallow tabletop depth of field, 12fps feel with slight jitter,
warm tungsten light.
```
Use for: charming explainers, food, education, unboxing metaphors.

## 8 · Retro film
```
STYLE: 16mm film, halation around highlights, heavy grain, slightly desaturated
with a warm bias, gate weave, soft vignette, vintage lens flare only from
on-screen sources.
```
Use for: nostalgia, heritage brands, music, memory.

## 9 · Night / neon
```
STYLE: night exterior, neon practicals in magenta and cyan, wet asphalt
reflections, deep blacks with visible detail, anamorphic bokeh, slow dolly.
```
Use for: tech, music, urban stories. Careful in 9:16 — keep neon off the face.

## 10 · Studio white / e-commerce
```
STYLE: seamless white or light-grey studio, soft even key with a large source,
clean shadow under the object, product centred, slow turntable, no props.
```
Use for: catalogues, marketplace listings, comparison shots.

## 11 · Editorial / archival
```
STYLE: archival collage, halftone textures, torn paper edges, muted sepia and
ink navy, overlaid grain, slow parallax, typewriter typography (overlay, not
generated).
```
Use for: history, journalism, essays.

## 12 · Anime / illustrated motion
```
STYLE: cel-shaded animation, clean line art, dramatic rim light, painted
backgrounds, limited animation on twos, speed lines only on impact.
```
Use for: fiction, gaming, younger audiences.

## 13 · Food / macro sensory
```
STYLE: 100mm macro, backlight for steam and texture, shallow focus pulling
through the subject, warm highlights, slow motion at 120fps feel, no hands.
```
Use for: recipes, restaurants, product texture.

## 14 · Data / motion graphic
```
STYLE: clean motion graphics, dark background, one accent colour, thin sans
type (overlay), lines and bars animating on a grid, no decorative shapes.
```
Use for: business, reports, news. Generate plates; typeset numbers yourself.

---

## Blending

Blend at most two, and state which wins where:
```
STYLE: documentary handheld base, with the colour discipline of a product
commercial — natural light, controlled contrast, no stylisation.
```

## Anti-slop checklist

The default AI look is glossy, over-saturated, over-lit and motion-sick. Remove it:

- [ ] Name the light source, not just "cinematic lighting"
- [ ] Specify one imperfection: grain, haze, slight overexposure, dust
- [ ] Fix the focal length (`35mm`, `50mm`, `100mm macro`)
- [ ] Keep one camera move
- [ ] Limit the palette to 3 colours
- [ ] Add `no lens flare, no HDR glow, no oversaturation, no perfect symmetry`
- [ ] Put humans off-centre; perfect centring reads as stock

## Style consistency across a series

Write the style block once into `assets/style-bible.md` for the project:

```
PALETTE: #0E1B26, #F2E9DA, #E4572E
LENS: 35mm, f/2
LIGHT: single window camera-left, practical bulb for warmth
GRAIN: light
TYPO: one heavy sans, white, 6% stroke
```
Then any future episode pastes from it. A series is recognised by its constraints, not its subjects.
