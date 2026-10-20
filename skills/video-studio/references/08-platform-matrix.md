# Platform matrix — one table to rule stages 1, 4 and 5

Verified October 2026. Platforms change specs; when a number matters for a paid campaign, re-check it and note the date.

## Video specs

| Platform | Aspect | Resolution | Max length | Sweet spot | Notes |
|---|---|---|---|---|---|
| YouTube Shorts | 9:16 (or 1:1) | 1080×1920 (min 720×1280) | 3 min | 15–60 s | MP4/H.264/AAC. 9:16 recommends itself |
| YouTube long-form | 16:9 | 1920×1080 or 3840×2160 | 12 h | 6–20 min | Chapters unlock session time |
| Facebook Reels | 9:16 | 1080×1920 (min 720×1280) | 90 s | 15–45 s | Native upload beats a link |
| Facebook feed video | 1.91:1 or 4:5 | 1080×1080 / 1200×630 | 240 min | 60–180 s | Mobile crops to 1:1 |
| Instagram Reels | 9:16 | 1080×1920 | 3 min | 15–45 s | Grid crops to 3:4 |
| Instagram feed | 4:5 | 1080×1350 | 60 min | 20–60 s | 4:5 takes the most feed height |
| TikTok | 9:16 | 1080×1920 | 10 min | 12–40 s | Profile grid crops to 1:1 |
| LinkedIn | 16:9 or 1:1 | 1920×1080 | 15 min | 30–120 s | Captions burned in; most watch muted |
| X | 16:9 or 1:1 | 1280×720 | 2:20 | 15–45 s | One idea per post |

## Thumbnail specs

| Platform | Size | Ratio | Cap | Crop to survive |
|---|---|---|---|---|
| YouTube long-form | 3840×2160 (1280×720 legacy) | 16:9 | 2 MB mobile / 50 MB desktop | full frame |
| YouTube Shorts | 2160×3840 | 9:16 | 2 MB | also a 16:9 crop |
| Facebook Reels cover | 1080×1920 | 9:16 | 30 MB | bottom 25% covered by UI |
| Facebook link | 1200×630 | 1.91:1 | 30 MB | mobile 1:1 |
| Instagram Reels cover | 1080×1920 | 9:16 | 8 MB | grid 3:4 |
| TikTok cover | 1080×1920 | 9:16 | 10 MB | grid 1:1 |
| LinkedIn | 1200×627 | 1.91:1 | 5 MB | full frame |
| X | 1280×720 | 16:9 | 5 MB | full frame |

## Copy limits

| Platform | Title | Body | Tags/hashtags | First visible line |
|---|---|---|---|---|
| YouTube | 100 | 5,000 | tags 500 chars, 3 hashtags | ~120 chars in search |
| Shorts | 100 | 5,000 | 3 hashtags | first frame + 2 lines |
| TikTok | caption 2,200 | same | 3–5 | ~100 chars before "more" |
| Instagram | caption 2,200 | same | 3–5 | ~125 chars |
| Facebook | post 63,206 | same | 0–2 | ~125 chars before "See more" |
| LinkedIn | post 3,000 | same | 3–5 | ~140 chars |
| X | 280 | same | 0–2 | whole post |

## Loudness and codec targets

| Target | Value |
|---|---|
| Integrated loudness (social) | **−14 LUFS** (range −16 to −13) |
| True peak | ≤ **−1.5 dBTP** |
| Codec | H.264 High, yuv420p, 30 or 60 fps |
| Audio | AAC-LC, 192 kbps, 48 kHz |
| Bitrate | 8–12 Mbps at 1080p |

## What each platform actually rewards

| Platform | Primary job | Optimise for | Kill these |
|---|---|---|---|
| YouTube Shorts | browse impressions | first 2 s + re-watch loop | slow open, logo, static end |
| YouTube long | search + suggested | title/description match with the promise | clickbait that the video does not pay off |
| TikTok | interest graph | retention curve, on-screen text, sound | links, watermarks from other apps |
| Instagram Reels | interest graph + shares | aesthetic consistency, cover text | reposted watermarked footage |
| Facebook | shares + comments | a sentence worth forwarding | vertical-only link posts |
| LinkedIn | credibility | the claim and the evidence | hype adjectives, emoji spam |
| X | conversation | one sharp idea | threads with no payoff |

## Cross-posting rules

1. **Never upload a file with another platform's watermark.** Re-export clean.
2. **Re-write the copy per platform.** Same video, different promise.
3. **Re-frame the thumbnail** — a 9:16 cover will be cropped everywhere else.
4. **Adjust the length** where the platform's sweet spot is far from yours (a 60 s Short can lose 15 s for Reels and gain retention).
5. **Post natively.** Links suppress reach on every visual platform.
6. **Stagger** by a few hours so comment replies do not collide.
7. **Keep one source of truth**: `publish-pack.md`, one section per platform, generated from the same storyboard.

## Quick platform picker

```
Children's content        → YouTube Shorts + Kids (mark Made for Kids), no TikTok
B2B / services           → LinkedIn + YouTube long
Local business           → Facebook Reels + Instagram Reels
Entertainment / music    → TikTok + Instagram Reels + Shorts
Product launch           → Shorts (reach) + Reels (aesthetic) + Facebook (share)
Search-driven education  → YouTube long + Shorts as the funnel
```
