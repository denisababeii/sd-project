# DESIGN.md — SF Films: Where Stories Find Their Place
*Visual & UX Design System for the San Francisco Cinema Data Story*

---

## 1. Design Philosophy

This website is a **data story, not a dashboard**. Every design decision must serve the narrative arc — guiding the reader from wonder, through discovery, to exploration. The aesthetic is **Art Deco refined for the screen**: geometric discipline, restrained luxury, and deliberate ornamentation — never gratuitous, always purposeful.

The tone is that of a **museum exhibition catalogue** that has been brought to life. Authoritative but not cold. Precise but not sterile. San Francisco deserves that treatment.

**The single most important UX principle:** The reader should never feel lost or overwhelmed. At any moment on the page, there is exactly one thing asking for their attention.

---

## 2. Color System

The palette draws from the physical textures of San Francisco itself: fog, gold rush, the bay at dusk, weathered terracotta.

```css
:root {
  /* Base */
  --color-void:       #0A0907;   /* Near-black warm. Page background. */
  --color-ink:        #1A1712;   /* Deep brown-black. Card backgrounds. */
  --color-surface:    #242018;   /* Raised surfaces, subtle panels. */

  /* Type */
  --color-parchment:  #F2EDE4;   /* Primary text. Warm white, never pure. */
  --color-fog:        #9A9589;   /* Secondary text, captions, metadata. */
  --color-ghost:      #4A4540;   /* Placeholder text, disabled states. */

  /* Gold — primary accent. Used sparingly. */
  --color-gold:       #C9883A;   /* Buttons, active states, key highlights. */
  --color-gold-light: #E8B96A;   /* Hover states, decorative lines. */
  --color-gold-mute:  #7A5128;   /* Subtle tints, inactive indicators. */

  /* Success factors — each factor has its own accent hue */
  --color-boxoffice:  #4A90C4;   /* Cool blue. Box office / commercial. */
  --color-awards:     #9B6EC8;   /* Purple. Awards / prestige. */
  --color-imdb:       #C4874A;   /* Amber-orange. IMDb / critical. */

  /* Sentiment spectrum — used in Section 5 */
  --color-sentiment-pos:    #6BAF8E;   /* Muted teal-green. Positive. */
  --color-sentiment-neu:    #9A9589;   /* Fog grey. Neutral. */
  --color-sentiment-neg:    #B05E5E;   /* Dusty rose-red. Negative. */

  /* Map heatmap range — applied as CSS gradient stops */
  --color-heat-low:   #1A1712;
  --color-heat-mid:   #7A5128;
  --color-heat-high:  #C9883A;
}
```

### Rules for Color Usage

- **Gold is precious.** Use it for one element per visual focal point — never two competing gold elements in the same viewport.
- **The three success-factor colors** (blue, purple, amber) must only appear in the context of their factor. Never decorate with them. The reader should learn to read these colors as a language.
- **Heatmaps** always use the heat gradient (`--color-heat-low` → `--color-heat-high`). Never use the success-factor colors for map fills — those are reserved for dots and labels.
- **White is banned.** The lightest value used is `--color-parchment`. Pure white feels clinical and breaks the aesthetic.

---

## 3. Typography

### Typeface Pairing

| Role | Family | Weight | Notes |
|---|---|---|---|
| **Display / Titles** | `Cormorant Garamond` | 300, 600 | Elegant, editorial. High-contrast strokes feel Art Deco without being theatrical. Use for section titles, the site name, and the introduction. |
| **Data Labels / Callouts** | `Josefin Sans` | 300, 400 | Geometric, spaced. Perfect for neighborhood names, fact labels, and legends. Its Art Deco letterform geometry ties the two families together. |
| **Body / Narrative** | `EB Garamond` | 400 | Readable long-form text. Warm and humanist. Used for step text, captions, and paragraph prose. |
| **Monospace / Numbers** | `DM Mono` | 300 | Numbers, statistics, axis labels. Monospaced keeps numeric alignment clean without feeling like code. |

### Type Scale

```css
:root {
  --text-display:   clamp(48px, 7vw, 96px);   /* Site title, hero headlines */
  --text-title:     clamp(28px, 4vw, 52px);   /* Section titles */
  --text-subtitle:  clamp(18px, 2.5vw, 28px); /* Sub-section heads */
  --text-body:      clamp(15px, 1.5vw, 18px); /* Narrative step text */
  --text-label:     12px;                      /* Map labels, legends */
  --text-micro:     10px;                      /* Axis ticks, metadata */

  --leading-tight:  1.1;
  --leading-body:   1.7;
  --leading-loose:  2.0;

  --tracking-tight: -0.02em;
  --tracking-wide:  0.12em;   /* Used on Josefin Sans labels — always uppercase + wide tracking */
  --tracking-ultra: 0.25em;   /* Decorative labels, section markers */
}
```

### Typography Rules

- Display headings in `Cormorant Garamond` **300** (light) for a refined, ethereal quality. **600** only for moments of emphasis.
- All `Josefin Sans` text is **uppercase + `--tracking-wide`**. No exceptions.
- Never mix more than two typefaces in a single viewport focal zone.
- Paragraph text line length: **55–70 characters max** (enforced via `max-width: 62ch`).

---

## 4. Layout & Grid

### Overall Structure

The site is a **single long-scroll page** with three layout modes that switch between sections:

1. **Full-bleed** — 100vw × 100vh. Used for the intro scene and map sections. The page disappears; only the content exists.
2. **Sticky map + scrolling steps** — Map locked to viewport left or center; narrative steps scroll on the right. The primary layout for Sections 2–4.
3. **Centered column** — max 760px centered. Used for the sentiment analysis narrative prose in Section 5.

```css
:root {
  --grid-max:       1280px;
  --grid-margin:    clamp(24px, 5vw, 80px);
  --steps-width:    38%;         /* Width of the scrolling step column */
  --map-max:        900px;       /* Max width of sticky map */
}
```

### Spacing System (8pt base)

```css
:root {
  --space-1:   8px;
  --space-2:   16px;
  --space-3:   24px;
  --space-4:   32px;
  --space-5:   48px;
  --space-6:   64px;
  --space-7:   96px;
  --space-8:   128px;
  --space-9:   192px;
}
```

### Z-Index Architecture

```css
:root {
  --z-background:   0;
  --z-map:          10;
  --z-heatmap:      20;
  --z-dots:         30;
  --z-steps:        40;    /* Step text always above map */
  --z-ui:           50;    /* Progress bar, nav */
  --z-overlay:      60;    /* Transitions, fades */
}
```

---

## 5. Art Deco Ornamental System

Art Deco is about **geometry as decoration** — but restraint is what separates it from kitsch. Use ornamental elements to mark transitions, frame section titles, and give the page a sense of craftsmanship.

### Decorative Rules

- **Section dividers:** A centered horizontal rule composed of a thin line — gold — interrupted at center by a small diamond or chevron motif. Never a plain `<hr>`.
- **Section markers:** Each section gets a small Josefin Sans label in `--color-gold` at `--text-micro` size, uppercase, with `--tracking-ultra`. Example: `◆ SECTION II`. This appears above the section title, left-aligned.
- **Corner brackets:** Used sparingly on featured stat cards or callout boxes. Four L-shaped lines in `--color-gold-mute` forming a border frame — not a full box, just the corners. CSS `::before` / `::after` with `box-shadow` or `border` tricks.
- **Step indicator line:** A vertical gold line (~1px) runs along the left edge of the step column during the sticky map sections, with the active step's dot glowing at `--color-gold`.
- **No shadows with color.** Box shadows use only `rgba(0,0,0,x)`. The gold glow on map dots is the single exception — kept to `box-shadow: 0 0 12px var(--color-gold)`.

### Geometric Background Texture

Sections that need depth (sentiment analysis, fusion map) use a **subtle geometric grid overlay** at `3–5% opacity` — a fine Art Deco fan or diamond lattice pattern, SVG-rendered as a `background-image`. Never visible at a glance; felt subliminally.

```css
.section--textured {
  background-image: url("assets/deco-lattice.svg");
  background-size: 120px 120px;
  background-repeat: repeat;
  /* The SVG is a thin-line diamond grid in #C9883A at 4% opacity */
}
```

---

## 6. Map Visual System

The map is the visual spine of the story. It must feel like a **cartographic artefact**, not a Google Maps embed.

### Base Map Treatment

```css
.map-img {
  filter: grayscale(100%) brightness(0.35) contrast(1.3) sepia(0.15);
  /* Result: a near-black map with warm undertones. Streets visible as faint lines. */
}
```

Neighborhood boundaries are overlaid as SVG paths — not the base image — so they can be colored independently.

### Dot System (filming locations)

```css
.film-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-gold);
  opacity: 0;                              /* Start invisible */
  box-shadow: 0 0 0 0 var(--color-gold);
  transition: opacity 0.4s ease, transform 0.4s ease;
}

.film-dot.appearing {
  opacity: 0.7;
  animation: pulse-dot 2s ease-out forwards;
}

.film-dot.active {
  opacity: 1;
  transform: scale(2.2);
  box-shadow: 0 0 16px var(--color-gold);
}

@keyframes pulse-dot {
  0%   { box-shadow: 0 0 0 0 rgba(201,136,58,0.6); }
  70%  { box-shadow: 0 0 0 10px rgba(201,136,58,0); }
  100% { box-shadow: 0 0 0 0 rgba(201,136,58,0); }
}
```

### Heatmap Neighborhood Fill

Each neighborhood `<path>` in the SVG gets a fill computed from the data value, mapped to the heat gradient. The fill transitions smoothly when switching between factors.

```css
.neighborhood-path {
  fill: var(--color-heat-low);
  stroke: rgba(242, 237, 228, 0.08);   /* Parchment at low opacity — subtle border */
  stroke-width: 0.5;
  transition: fill 0.8s ease;
}

.neighborhood-path:hover {
  stroke: var(--color-gold-light);
  stroke-width: 1.5;
  cursor: pointer;
}
```

The **highlighted neighborhood** (the one referenced by the current step) gets:
- A gold stroke at `stroke-width: 2`
- A gold dot marker at its centroid
- A small label card appearing beside it (see Callout Cards below)

### Factor Color Dots (Section 3)

When a fact references a specific factor, the highlighted neighborhood dot shifts color to the factor accent:

```css
/* Applied dynamically via JS class toggling */
.dot--boxoffice { background: var(--color-boxoffice); box-shadow: 0 0 14px var(--color-boxoffice); }
.dot--awards    { background: var(--color-awards);    box-shadow: 0 0 14px var(--color-awards); }
.dot--imdb      { background: var(--color-imdb);      box-shadow: 0 0 14px var(--color-imdb); }
```

### Callout Cards (Map Annotations)

Small floating cards anchored near the highlighted neighborhood. Minimal: one number, one label.

```css
.map-callout {
  position: absolute;
  background: var(--color-ink);
  border: 1px solid var(--color-gold-mute);
  padding: var(--space-2) var(--space-3);
  font-family: 'Josefin Sans', sans-serif;
  font-size: var(--text-label);
  letter-spacing: var(--tracking-wide);
  text-transform: uppercase;
  color: var(--color-parchment);
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.4s ease;

  /* Corner bracket effect */
  &::before, &::after {
    content: '';
    position: absolute;
    width: 8px; height: 8px;
    border-color: var(--color-gold);
    border-style: solid;
  }
  &::before { top: -1px; left: -1px; border-width: 1px 0 0 1px; }
  &::after  { bottom: -1px; right: -1px; border-width: 0 1px 1px 0; }
}

.map-callout.visible { opacity: 1; }
```

---

## 7. Scrollytelling Step Text

Step cards are the narrative voice. They must be readable, unfussy, and feel like a knowledgeable guide speaking — not a slide deck.

```css
.step {
  max-width: 380px;
  margin-bottom: 60vh;
  opacity: 0.12;
  transform: translateY(12px);
  transition: opacity 0.5s ease, transform 0.5s ease;
}

.step.active {
  opacity: 1;
  transform: translateY(0);
}

/* Section marker above each step */
.step__marker {
  font-family: 'Josefin Sans', sans-serif;
  font-size: var(--text-micro);
  letter-spacing: var(--tracking-ultra);
  text-transform: uppercase;
  color: var(--color-gold);
  margin-bottom: var(--space-2);
}

/* The stat / highlight number */
.step__stat {
  font-family: 'DM Mono', monospace;
  font-size: clamp(28px, 3vw, 40px);
  color: var(--color-parchment);
  font-weight: 300;
  line-height: 1;
  margin-bottom: var(--space-2);
}

/* Narrative prose */
.step__body {
  font-family: 'EB Garamond', serif;
  font-size: var(--text-body);
  line-height: var(--leading-body);
  color: var(--color-fog);
  max-width: 58ch;
}

/* Hook — the trailing question or tension */
.step__hook {
  font-family: 'Cormorant Garamond', serif;
  font-size: clamp(16px, 1.8vw, 20px);
  font-style: italic;
  color: var(--color-parchment);
  margin-top: var(--space-3);
  font-weight: 300;
}
```

### Step Anatomy

Each step should be built from these elements in order:

```
◆ FACTOR LABEL          ← .step__marker (e.g. "◆ BOX OFFICE")
$115,000,000            ← .step__stat
Lone Mountain leads...  ← .step__body (2–3 sentences max)
But why does prestige   ← .step__hook (the question pulling forward)
cluster here?
```

---

## 8. Sentiment Section Typography & Charts

The sentiment section shifts register — from map-driven to chart-driven. The layout narrows to a centered column and the mood becomes more contemplative.

### Section Transition

A full-viewport **fade-to-black** transition (0.8s) marks the shift from the map world to the sentiment world. A brief title card appears:

```
◆ SECTION V

What the stories said.
```

Then the content fades in beneath.

### Sentiment Bar / Distribution Charts

Keep chart chrome to an absolute minimum:

- No gridlines — use subtle dotted rules at `rgba(242,237,228,0.08)` only
- No borders on chart containers
- Axis labels in `DM Mono` at `--text-micro`, color `--color-ghost`
- Bar fills use the three factor colors (`--color-boxoffice`, `--color-awards`, `--color-imdb`) with `0.85` opacity
- Sentiment spectrum bars use the sentiment colors (`--color-sentiment-pos/neu/neg`)
- Animate bars growing from zero on scroll entry (CSS `@keyframes` width expansion, `0.6s ease-out`, staggered by `0.1s` per bar)

### TF-IDF Word Display

Use a **restrained word arrangement** — not a chaotic word cloud. Words arranged in order of weight, displayed as a typographic list with size scaled by TF-IDF score. Each word in `Cormorant Garamond` italic, color shifting from `--color-fog` (low weight) to `--color-parchment` (high weight). The dominant word for each success category appears in its factor color.

---

## 9. Interactive Map Section

The final map is the same cartographic treatment as the story map, but the frame changes: the narrative columns are gone, the map expands to near-full screen, and control panels appear.

### Filter Panel

```css
.filter-panel {
  position: absolute;
  top: var(--space-5);
  left: var(--space-5);
  background: rgba(26, 23, 18, 0.92);
  backdrop-filter: blur(8px);
  border: 1px solid var(--color-gold-mute);
  padding: var(--space-4);
  min-width: 240px;
}
```

- Factor toggles: three pill buttons, one per factor color. Inactive = outlined; active = filled.
- Year range: a minimal custom range slider in gold.
- Genre filter: a dropdown in `Josefin Sans` styling.

### Tooltip on Hover

```css
.map-tooltip {
  background: var(--color-ink);
  border-top: 2px solid var(--color-gold);
  padding: var(--space-2) var(--space-3);
  font-family: 'EB Garamond', serif;
  font-size: var(--text-body);
  /* Contains: neighborhood name, key stats per active factor */
}
```

---

## 10. Motion & Animation Principles

| Moment | Animation | Duration | Easing |
|---|---|---|---|
| Dot appearing (density map) | Fade + pulse | 0.4s + 2s | ease-out |
| Step text activating | Fade + translateY(12px→0) | 0.5s | ease |
| Heatmap color transition | Fill color shift | 0.8s | ease |
| Section transition | Full-page fade to black | 0.8s | ease-in-out |
| Fusion map assembly | Heatmaps slide together + blend | 1.2s | ease-in-out |
| Chart bars growing | Width 0 → value | 0.6s staggered | ease-out |
| Callout card appearing | Opacity 0 → 1 | 0.4s | ease |

### Motion Rules

- **Respect `prefers-reduced-motion`.** All animations must have a `@media (prefers-reduced-motion: reduce)` override that disables transitions and shows states directly.
- No looping animations in the background while the reader is trying to read. Dots pulse once on arrival; they do not breathe or loop.
- The fusion map animation (Section 4) is the single most elaborate animation on the page — treat it as a cinematic beat. It earns its complexity because it is a narrative climax, not a decorative flourish.

---

## 11. Progress Indicator

A minimal vertical progress bar on the far right edge of the viewport. Thin (2px), gold, grows as the user scrolls. Section names appear as small labels beside it at their corresponding scroll positions — visible only on hover.

```css
.progress-rail {
  position: fixed;
  right: var(--space-3);
  top: 10vh;
  height: 80vh;
  width: 1px;
  background: var(--color-ghost);
  z-index: var(--z-ui);
}

.progress-fill {
  width: 100%;
  background: var(--color-gold);
  transition: height 0.1s linear;
}
```

---

## 12. Accessibility

- Minimum contrast ratio: **4.5:1** for all body text against its background. `--color-fog` on `--color-void` is the lowest contrast pair — verify it passes.
- All map interactions must have keyboard equivalents. Neighborhood selection via arrow keys when the interactive map is focused.
- Heatmap color alone must never be the sole carrier of information — always pair with a numeric label or pattern.
- `aria-live` regions for step text changes so screen readers announce narrative progression.
- All animated elements respect `prefers-reduced-motion`.

---

## 13. Asset & File Conventions

```
/assets
  /fonts          ← Self-hosted WOFF2 files
  /map
    sf-base.svg           ← Grayscale base map
    sf-neighborhoods.svg  ← Neighborhood boundary paths (named by ID)
    deco-lattice.svg      ← Repeating background texture
  /icons
    diamond.svg           ← Section marker ornament
    bracket-tl.svg        ← Corner bracket (top-left)
    bracket-br.svg        ← Corner bracket (bottom-right)
/styles
  tokens.css        ← All CSS variables (this file)
  typography.css
  layout.css
  map.css
  steps.css
  sentiment.css
  interactive.css
  motion.css
  accessibility.css
```

---

## 14. What This Design Must Never Do

- Use a white or near-white background anywhere in the scrollytelling sections.
- Show more than one highlighted neighborhood simultaneously during the step narrative.
- Use animation to decorate rather than to explain.
- Let the map become a generic choropleth — the cartographic treatment (dark, warm, with dot language) must be maintained throughout.
- Use color for aesthetic variety — every color on screen is doing semantic work.
- Let any section feel like a PowerPoint slide. If it can be summarized as "bullet points over a background," redesign it.

---

*This document is a living reference. Update token values here first; never hardcode values in component files.*
