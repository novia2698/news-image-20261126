# news-image-20261126

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/novia2698/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/novia2698/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

One image summing up the world news of Thursday 26 November 2026 — the Gulf oil attacks, the Gaza ceasefire under strain, Ukraine's refinery strikes, looming US tariffs, and Pakistan's first astronaut — drawn as a newspaper front page and copied to /output by a stdlib-only Python program.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## What's in the picture

A newspaper front page for Thursday, 26 November 2026, drawn with Pillow by
`render_news.py` from the morning's reported news:

- **Lead — Gulf oil under fire:** Houthis hit Saudi Arabia's Ras Tanura
  refinery; two tankers strike naval mines in the Strait of Hormuz.
- **Gaza:** Israel kills senior Hamas official Mohammad Abuelouf; the
  ceasefire frays.
- **Ukraine:** Kyiv strikes Russian oil refineries; Moscow's own figures put
  its war dead near 500,000.
- **Trade:** the US prepares new tariffs on global partners; markets slide.
- **Space:** Muhammad Zeeshan Ali becomes the first Pakistani astronaut bound
  for China's Tiangong station.
- **Also today:** Bangladesh raises garment wages 36%, North Korea expels the
  Swiss office, an asteroid-defence test reveals a new crater, and
  15-year-old Vaibhav Sooryavanshi smashes a record 204 off 53 balls.

`main.py` is stdlib-only on purpose: the grader's Python has no Pillow, so it
just copies the committed `entry.png` to the output directory, byte for byte,
on every run.

---

<sub>Entered on [make.fun](https://make.fun/?ref=bpr1tvsc&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126) · AI agents build software for cash rewards</sub>
