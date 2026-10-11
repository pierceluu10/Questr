---
name: Questr
description: A daily field journal for small everyday adventures.
colors:
  paper: "#f7f5ed"
  surface: "#fffef8"
  ink: "#233e32"
  body: "#60685f"
  line: "#d9ddd0"
  green: "#244c3a"
  green-soft: "#e3eadd"
  clay: "#935440"
  clay-soft: "#f3e3d9"
  honey: "#866326"
  honey-soft: "#f3ebd1"
  dark-paper: "#17251e"
  dark-surface: "#203027"
  dark-ink: "#f0eedf"
  dark-body: "#b8c4b7"
  dark-line: "#415044"
  dark-green: "#bbd4aa"
  dark-green-soft: "#354c36"
  dark-clay: "#edb199"
  dark-clay-soft: "#4e382e"
  dark-honey: "#e8cb85"
  dark-honey-soft: "#4b422e"
typography:
  display:
    fontFamily: 'Georgia, "Times New Roman", serif'
    fontSize: "clamp(66px, 6.5vw, 94px)"
    fontWeight: 400
    lineHeight: 1.08
    letterSpacing: "-0.04em"
  headline:
    fontFamily: 'Georgia, "Times New Roman", serif'
    fontSize: "52px"
    fontWeight: 400
    lineHeight: 1.08
    letterSpacing: "-0.04em"
  title:
    fontFamily: 'Georgia, "Times New Roman", serif'
    fontSize: "27px"
    fontWeight: 400
    lineHeight: 1.3
    letterSpacing: "-0.025em"
  operational-title:
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'
    fontSize: "17px"
    fontWeight: 600
    lineHeight: 1.08
    letterSpacing: "-0.02em"
  body:
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.65
  journal-entry:
    fontFamily: 'Georgia, "Times New Roman", serif'
    fontSize: "23px"
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'
    fontSize: "12px"
    fontWeight: 600
    lineHeight: 1.65
  button:
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'
    fontSize: "13px"
    fontWeight: 600
    lineHeight: 1.4
rounded:
  field: "6px"
  button: "7px"
  notice: "8px"
  sheet: "10px"
  panel: "12px"
  invitation: "16px"
  circle: "50%"
spacing:
  label-gap: "8px"
  field-padding: "12px"
  compact-gap: "16px"
  row-gap: "20px"
  surface-padding: "24px"
  rail-padding: "28px"
  form-padding: "36px"
  app-gap: "42px"
  page-gutter: "48px"
components:
  button-primary:
    backgroundColor: "{colors.green}"
    textColor: "{colors.paper}"
    typography: "{typography.button}"
    rounded: "{rounded.button}"
    padding: "15px 24px"
  button-small:
    backgroundColor: "{colors.green}"
    textColor: "{colors.paper}"
    typography: "{typography.button}"
    rounded: "{rounded.button}"
    padding: "11px 16px"
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.green}"
    typography: "{typography.button}"
    rounded: "{rounded.button}"
    padding: "15px 24px"
  field:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.field}"
    padding: "{spacing.field-padding}"
    width: "100%"
  chart-card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sheet}"
    padding: "{spacing.surface-padding}"
  form-surface:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.panel}"
    padding: "{spacing.form-padding}"
  progress-rail:
    backgroundColor: "{colors.green-soft}"
    textColor: "{colors.ink}"
    rounded: "{rounded.panel}"
    padding: "{spacing.rail-padding}"
  category-social:
    backgroundColor: "{colors.clay-soft}"
    textColor: "{colors.clay}"
    rounded: "{rounded.circle}"
    size: "42px"
  category-health:
    backgroundColor: "{colors.green-soft}"
    textColor: "{colors.green}"
    rounded: "{rounded.circle}"
    size: "42px"
  category-mindfulness:
    backgroundColor: "{colors.honey-soft}"
    textColor: "{colors.honey}"
    rounded: "{rounded.circle}"
    size: "42px"
---

# Design System: Questr

## Overview

**Creative North Star: "The Daily Field Journal"**

Questr feels like a warm, well-kept journal for small everyday adventures. Cream paper, forest ink, ruled entries and a botanical seal make its world tangible. Georgia carries the invitation and personal writing; a clean system sans keeps tasks, forms and progress easy to scan.

The interface is generous without making action feel distant. Category color gives each quest a recognizable place, while the app presents actual quests, reflections and earned progress plainly. The landing journal is explicitly marked as an example day; the operational screens use persisted user data.

**Key Characteristics:**
- Warm paper and forest tones with clay and honey category accents.
- Editorial Georgia headings paired with practical sans-serif controls.
- Flat ruled entries, softly bounded forms and charts, and one illustrated journal surface.
- Visible navigation, direct actions and a quiet record of progress.

## Colors

The palette pairs warm near-white paper with botanical green and earthy category colors. The frontmatter is normative; CSS exposes the light roles as matching custom properties and remaps those same properties for dark appearance.

### Primary
- **Forest (`green`):** primary buttons, links, the Health category, the progress fill and sentiment chart stroke.
- **Leaf wash (`green-soft`):** progress panels, the landing invitation, Health markers and the sentiment chart fill.

### Secondary
- **Clay (`clay` / `clay-soft`):** the Social category and field validation messages; its pale wash supports the category symbol.
- **Honey (`honey` / `honey-soft`):** the Mindfulness category and XP values; its pale wash supports the category symbol.

### Neutral
- **Cream paper (`paper`):** the page and input background.
- **Open sheet (`surface`):** the journal preview, forms and chart cards.
- **Forest ink (`ink`):** headings, personal reflections and primary text.
- **Soft graphite (`body`):** descriptions, dates, hints and supporting information.
- **Pencil rule (`line`):** divisions, input strokes, chart guides and the unfilled progress track.

### Named Rules

**The Category Continuity Rule.** Social stays clay, Health stays green and Mindfulness stays honey across symbols, labels and charts; always pair color with text.

**The Same Roles Rule.** Dark appearance remaps the existing roles through `:root[data-theme="dark"]`; preserve the hierarchy rather than adding a separate visual language.

The `dark-*` frontmatter tokens correspond one-to-one to their light roles. The illustrated journal cover retains its fixed forest-and-cream artwork in either appearance; its pale botanical stroke is artwork, not a general interface token.

## Typography

**Display Font:** Georgia, with Times New Roman and serif fallbacks.

**Body Font:** the platform system sans, with Segoe UI and sans-serif fallbacks.

**Character:** familiar book typography gives invitations and reflections a personal voice. Sans-serif labels and supporting text keep repeated actions precise. Italic emphasis is forest-colored and remains regular weight.

### Hierarchy
- **Display:** the landing headline uses the frontmatter display role; on narrow screens it settles at (70px).
- **Headline:** app headings use the headline role, becoming (43px) at the mobile breakpoint. Form introductions use (54px) on desktop and (43px) on mobile.
- **Section headings:** landing sections use Georgia at (48px), becoming (39px); the final invitation uses (58px), becoming (44px).
- **Title:** quest names use the title role, becoming (24px) on mobile. Category titles use the same size with slightly looser tracking (-0.02em).
- **Operational title:** task and journal section headings use the sans-serif role; chart headings use (16px) with the same weight and tracking.
- **Body:** the base uses the body role. Hero copy uses (16px / 1.85) and a (40ch) measure; quest descriptions use (13px / 1.8) and a (55ch) measure.
- **Journal entry:** personal reflection text uses the journal-entry role, giving saved words more presence than metadata.
- **Label:** fields use the label role; buttons use their own compact role. Small uppercase category labels identify data categories, while dates, hints and totals remain quiet supporting text.

### Named Rules

**The Two Voices Rule.** Use Georgia for invitation, quest titles and personal writing; use the system sans for controls, descriptions and operational headings.

## Layout

Header, footer and page share a centered maximum width (1360px) with desktop gutters (48px). Mobile gutters become (24px). Most app content is separated by rules rather than repeated cards.

The desktop landing hero uses two columns (0.95fr / 1.05fr), a gap (64px) and generous block padding (82px / 120px). The three category columns use a gap (48px). Forms use two equal columns within (1000px), with a gap (100px), introductory text on the left and a bounded form on the right.

Today and My journal use a flexible main column and a progress rail (280px), separated by (42px). At (1100px) the rail becomes (240px), the gap becomes (28px), and the chart grid changes from (1.2fr / 1fr) to one column. Chart plots retain a dedicated height (220px), with summaries outside the plot.

At (760px), landing, forms and app layouts become one column. Tasks stay before progress; the journal's charts, reflections and achievements stay before its progress panel. The progress statistics become three adjacent columns, and the supporting rail note is omitted. Form surfaces use mobile padding (24px). The preview sheet loses its rotation while the illustrated cover keeps its angle. At (400px), navigation can wrap and preview spacing tightens.

**The Reading Order Rule.** Keep task and journal content first in document order, with progress afterward; preserve that order when columns collapse.

## Elevation & Depth

Most of Questr is flat: pencil rules separate entries and tonal washes distinguish supporting surfaces. Forms and charts use thin borders without elevation. Only the illustrative journal sheet receives the ambient `--shadow` defined in the sidecar; dark appearance removes it. The rotated cover and sheet provide depth for the illustration, not a general card treatment.

**The Journal Exception Rule.** Reserve ambient shadow and stacked rotation for the illustrated journal; app records, forms and charts remain grounded.

## Shapes

Thin rules and modest rounded corners soften the journal without making it toy-like. Fields and progress tracks use the field radius; buttons use the button radius. Forms and progress panels share the panel radius, while charts and the illustrated sheet share the sheet radius. The wide landing invitation uses its larger invitation radius.

Category symbols and the theme control are circles. Category icons are inline SVG strokes (22px), drawn with the category's current text color. The wordmark uses a stroked leaf; the journal illustration uses its own botanical seal. Preserve these vectors rather than introducing an unrelated icon family.

## Components

### Buttons

Quiet, legible actions with a forest fill and cream label. The primary and small variants use the frontmatter padding and radius; the small variant tightens the icon gap to (18px), compared with (28px) for the primary. Secondary actions use a transparent fill with a forest label and border.

Hover lowers opacity to (0.86) over (150ms). Pressing offsets the button down (1px). Keyboard focus uses a forest outline (3px) separated by (4px). Reduced motion disables transitions; the pressed state remains immediate. Text links keep a forest underline offset (4px).

### Cards / Containers

Forms and chart cards are open-sheet surfaces with a single pencil-rule border. Padding follows their frontmatter roles. Flash messages use a leaf wash and notice radius, with `role="status"`. Empty states use plain supporting copy and a direct next step rather than a decorative container.

### Inputs / Fields

Full-width cream fields use a pencil-rule border, the field radius, and ink text. Labels sit above with an (8px) gap. Invalid fields switch the border to clay; a textual error list sits below and is associated through `aria-describedby`. Hints remain visible and use supporting text color.

Use the existing `field` macro from `templates/forms.html` for authentication and reflection fields. Preserve the Flask forms, `form.hidden_tag()` CSRF fields, labels, autocomplete, error associations and textarea rows. The sidecar field is a visual example, not a replacement form implementation.

### Navigation

The leaf wordmark anchors the left; navigation and appearance control sit on the right. The current app link is forest-colored and underlined with an (8px) offset. Other links underline on hover. Today, My journal and Log out remain available on narrow screens; only the signed-out header's small signup action is hidden at the mobile breakpoint.

The theme button announces the next appearance and exposes its pressed state. Its SVG stays the same while the palette changes. Appearance is saved locally when storage is available. The skip link becomes visible on keyboard focus.

### Category Markers and Quest Rows

Social uses an outward arrow, Health a pulse line and Mindfulness a sun, all supplied by the shared SVG macro. Each marker is paired with its category name. Rows use symbol / flexible content / XP columns, separated by top rules and generous block padding (28px). Titles lead; descriptions and completion or reflection actions follow. Completed quests mute the title and show explicit completion text.

### Progress Rail

A leaf-wash panel carries the encouraging heading, large serif level number, a labeled progress bar and actual totals. The progress track is (6px) tall. Keep its accessible progressbar values and label. Desktop statistics are ruled pairs; mobile statistics sit in three columns with the value above its label.

### Journal Charts and Entries

Both chart cards use the same container pattern. The sentiment chart is a forest line and leaf fill; completed-category segments use the category palette. Text summaries remain outside the canvas. Loading, empty, unavailable and request-failure states occupy the same plot area and provide readable status copy. Theme changes update chart colors without animation; reduced motion disables chart animation.

Saved reflections use serif text below a row of date and sentiment metadata. Achievements use compact sans-serif titles, descriptions and earned dates. Preserve the sentiment explanation as a guide rather than a clinical measure.

### Illustrated Journal

The landing preview combines a fixed forest cover, botanical SVG and open sheet, rotated (-4deg / 1.5deg) on desktop. Its three ruled sample quests communicate the category system. Keep the visible “Example day” badge and illustrative accessible label; this surface must not resemble invented account data.

## Do's and Don'ts

### Do:
- **Do** reuse the paper, ink, line and category custom properties in both appearances.
- **Do** keep Georgia for invitations, quest titles and reflection text, and the system sans for controls and task detail.
- **Do** preserve the category SVGs alongside readable category labels.
- **Do** keep tasks and journal content before progress when the layout stacks.
- **Do** retain visible Log out navigation, keyboard focus, field errors, CSRF forms and chart status text.
- **Do** identify the landing journal as an example and derive app progress from persisted data.

### Don't:
- **Don't** extend the journal illustration's shadow or rotation to ordinary app containers.
- **Don't** replace ruled quest and reflection entries with a grid of decorative cards.
- **Don't** communicate category, completion, validation or chart meaning through color alone.
- **Don't** turn small data labels into invented promotional kickers above headings.
- **Don't** add a new icon family, hide operational navigation on mobile, or remove reduced-motion behavior.
- **Don't** present sentiment as a clinical measure or invent testimonials, pricing or measured outcomes.
