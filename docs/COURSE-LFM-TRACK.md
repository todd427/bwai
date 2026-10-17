# <span style="color:#1F3A5F">BWAI Local — the on-device track</span>

<span style="color:#7F8C8D">**Owner:** Todd McCaffrey · **Date:** 2026-10-17 · **Status:** Course design, proposed · **Working name:** BWAI Local (Irish name to be chosen; check with Ainm first)</span>
<span style="color:#7F8C8D">**Relation to BWAI:** a parallel six-week track with the same shape (5 sessions/week, Sunday project, Anseo peer review) and the same licence (CC BY-SA 4.0 content, MIT code). Where BWAI uses the Claude API, this track runs Liquid AI's LFM2.5 models in the student's own browser over WebGPU. No API key, no per-token cost, no server.</span>

---

## <span style="color:#16A085">1. The pitch</span>

*Build AI features that run on the machine in your pocket.* Every project in this track ships as a static page that downloads a model once and runs it locally. The student finishes with a portfolio of deployed, working, zero-cost AI apps and a working understanding of what a small model can and cannot do, learned by watching one fail.

**Why this track exists.** BWAI teaches engineers to build with a frontier model behind an API. That is the right first course, but it hides three things a working engineer needs to know: what inference costs, where the model's limits are, and what happens when the network is gone. A 1.2B-parameter model running on a laptop GPU makes all three visible every session.

**Position against BWAI.** Not a replacement and not a beginner version. Same entry bar (Python, Git, a terminal, now plus basic JavaScript). A student can take either track first; the two share Week 0 habits and the Anseo community. Taking both gives the full picture: frontier-via-API and small-on-device.

---

## <span style="color:#16A085">2. What runs in the browser (verified 2026-10-17)</span>

All models below are Liquid AI ONNX exports under the **LFM Open License v1.0** (Hugging Face tag `lfm1.0`). Liquid's pricing page states research and education use is free with no revenue threshold; the full licence text is linked from each model repo and has not been read for this document.

| Model (Hugging Face id) | What it is | Browser build | Download | Use in track |
|---|---|---|---|---|
| `LiquidAI/LFM2.5-350M-ONNX` | smallest chat model | WebGPU-tagged; transformers.js | not stated on card | Week 0 smoke test; low-end device fallback |
| `LiquidAI/LFM2.5-1.2B-Instruct-ONNX` | main chat model | Q4 or FP16 on WebGPU (Q8 not supported) | Q4 ~1.2 GB, FP16 ~2.4 GB | Weeks 1–5 default model |
| `LiquidAI/LFM2.5-1.2B-Thinking-ONNX` | same size, reasoning traces | WebGPU-tagged | not stated on card | Week 1 thinking-vs-not comparison |
| `LiquidAI/LFM2.5-VL-450M-ONNX` | vision-language | FP16 encoder + Q4 decoder on WebGPU | ~770 MB | Week 3 vision feature |
| `LiquidAI/LFM2.5-2.6B-ONNX` | agentic / tool-calling | WebGPU-tagged; Liquid runs a WebGPU Space for it | not stated on card | Week 5 agents, if the device can carry it |

**The library.** `@huggingface/transformers` (transformers.js v4+). The text models load with `AutoModelForCausalLM.from_pretrained(id, { device: "webgpu", dtype: "q4" })`; the vision model with `AutoModelForImageTextToText` and a per-component dtype map (`vision_encoder: "fp16"`, `embed_tokens: "fp16"`, `decoder_model_merged: "q4"`). Both snippets are on the model cards and are what Week 2's sessions are built from.

**Browser.** WebGPU in Chrome or Edge; the model cards still point students at `chrome://flags/#enable-unsafe-webgpu` and `navigator.gpu.requestAdapter()` as the check. Week 0 turns that into a one-page test.

**Hardware floor.** <span style="color:#C0392B">Not yet measured.</span> Liquid publishes phone numbers for a Galaxy S26 Ultra and nothing for older handsets. Before launch: run the Week 0 page on Lava (laptop), the S22 Ultra, and one deliberately weak machine, and record tokens/s for 350M and 1.2B-Q4. The 350M model is the floor; a student whose device cannot run it at usable speed takes the **CPU lane** (§6).

---

## <span style="color:#16A085">3. What changes from BWAI</span>

| | BWAI | BWAI Local |
|---|---|---|
| Model | Claude via API | LFM2.5 in the browser |
| Accounts | GitHub, Anthropic, Railway, Anseo | GitHub, Anseo |
| Cost to student | a few euro of API credit | zero |
| Dev environment | Codespaces | Codespaces for editing and Git; the page itself runs in the student's own browser on their own GPU |
| Deploy target | Railway | GitHub Pages (static) |
| Language | Python | JavaScript in the page; Python only in the CPU lane and the Week 4 index builder |
| Week 2 | AI-augmented coding | Build the pocket chat (the runtime every later week reuses) |
| What you learn that BWAI can't teach | — | cost, limits, offline |

The `bwai` CLI gains three commands (`webgpu-check`, `new-page`, `pages-deploy`); spec in §7.

---

## <span style="color:#16A085">4. The six weeks</span>

Format per week: five sessions of 30–45 minutes, one concept + one exercise + one output each, then a weekly project due Sunday on Anseo. Session text below is the outline the full session docs are written from.

### <span style="color:#2980B9">Week 0 — Launch Pad</span>

**Goal:** a model has generated text on your own hardware and you know how fast.

1. **Accounts.** GitHub (professional username; Student Pack for Codespaces hours), Anseo (join *BWAI Local*). No Anthropic key, no Railway.
2. **Open the Codespace, run `bwai webgpu-check`.** It prints a URL; open it in Chrome/Edge *on the device you'll use for the course*. The page reports adapter name, max buffer size, and whether WebGPU is on.
3. **First inference.** The same page loads `LFM2.5-350M-ONNX`, asks one fixed question, and prints tokens/s. Post the number on Anseo in the *Benchmarks* thread with your device. This thread becomes the course's own hardware table.
4. **Scaffold.** `bwai new-page hello-local --week 1` creates `projects/week1/hello-local/index.html` with the model loader already wired. Change the prompt, reload, commit, push.
5. **Introductions** on Anseo, plus one reply.

**Checklist** mirrors BWAI's Week 0 with the Anthropic/Railway lines removed and the benchmark post added.

### <span style="color:#2980B9">Week 1 — Thinking With a Small Model</span>

**Goal:** know where a 1.2B model breaks, from your own evidence.

1. **What 1.2B parameters buys.** Load `LFM2.5-1.2B-Instruct-ONNX` (Q4, ~1.2 GB; it caches). Same question as Week 0; compare the answer and the speed to 350M.
2. **The probe set.** Twelve prompts across arithmetic, recent facts, long instructions, code, a private fact about yourself, and a trick question. Run all twelve on 350M and 1.2B. Record pass/fail in a table. (Optional: run the same twelve through any frontier model you already have access to, in a browser tab, and add a column. Not required.)
3. **Thinking on, thinking off.** Swap in `LFM2.5-1.2B-Thinking-ONNX`. Same twelve. Count the tokens spent in the reasoning trace against the answer. Find a prompt where thinking fixed the answer and one where it only cost time.
4. **Reading the fuzz.** Confident wrong answers, loops, refusals, format drift — the four failure shapes, with the student's own examples from sessions 2–3 as the material.
5. **The collaboration charter**, as in BWAI, now with a line for *what I will never trust a local model with*.

**Project:** `failure-catalogue` — a static page showing your twelve prompts, three models, and verdicts, with one paragraph per failure shape. Deploy to GitHub Pages, post on Anseo, review two peers.

### <span style="color:#2980B9">Week 2 — Build the Pocket Chat</span>

**Goal:** a chat page you built, installable on your phone, that you'll reuse for the rest of the course.

1. **Anatomy of the loader.** `AutoModelForCausalLM.from_pretrained` with `device: "webgpu"`, `dtype: "q4"`; progress callback; the browser cache; why the first load is slow and the second is not.
2. **Chat template and streaming.** `tokenizer.apply_chat_template` with `return_dict: true`; `TextStreamer` with `skip_prompt`; render tokens as they arrive.
3. **The cost meter.** Time to first token, tokens/s, total tokens, and — for the Thinking model — the share of output spent inside the reasoning trace. Shown in the UI on every reply. This meter is the track's teaching instrument and every later project keeps it.
4. **Make it a PWA.** Manifest, service worker that caches the page (the model is already in the browser cache), install to home screen. Test on your phone.
5. **Model picker and system prompt.** Switch between 350M, 1.2B and 1.2B-Thinking without reload; a system prompt field; save both in `localStorage`.

**Project:** `pocket-chat` — deployed, installed on your phone, with a screenshot of the cost meter in your Anseo post. This page is the base for Weeks 3–5.

### <span style="color:#2980B9">Week 3 — An AI Feature That Sees</span>

**Goal:** a vision feature, on-device, with structured output you can act on.

1. **Load the VL model.** `AutoModelForImageTextToText` + `AutoProcessor` for `LFM2.5-VL-450M-ONNX`, per-component dtypes, `RawImage` from a file input or the camera.
2. **Describe, then extract.** Free caption first; then a prompt that demands a fixed shape ("answer with exactly: label, confidence low/medium/high, one-line reason"). Parse it. Measure how often the shape holds.
3. **Getting JSON out of a small model.** Prompt-side discipline, a validator, and a retry-once loop. Where it still fails, fall back to a free-text field rather than lying with a parsed default.
4. **Batch and UX.** Drop ten images; a queue; a progress bar; results in a table; export CSV. The cost meter reports seconds per image.
5. **Privacy as the feature.** Nothing leaves the device. Write the one-paragraph privacy statement for your page and put it on the page.

**Project:** one of — a receipt reader that outputs date/vendor/total, a photo sorter that labels a folder of images against categories the user types, or a whiteboard-to-text page. Deployed, with the structured-output hit rate reported honestly in the post.

### <span style="color:#2980B9">Week 4 — RAG With No Server</span>

**Goal:** question-answering over your own documents, entirely client-side.

1. **Why retrieval.** Week 1 showed the model doesn't know your private fact. Give it the page that does.
2. **Chunk and embed in the browser.** A sentence-embedding model via transformers.js, chunks in IndexedDB, cosine search in plain JS. <span style="color:#C0392B">Gap:</span> no Liquid ONNX export of `LFM2.5-Embedding-350M` was found on the Hub on 2026-10-17, so this session uses a browser-ready embedder from another publisher. Revisit before launch; if Liquid ships one, switch.
3. **Ground the prompt.** Top-k chunks into the system prompt with citations; the model answers *only from the passages* or says it can't. Measure refusal-when-absent on five questions whose answers aren't in the corpus.
4. **Evaluate.** Ten questions with known answers; hit rate with and without retrieval; the cost meter now shows retrieval time alongside generation.
5. **Index once, carry anywhere.** Export the index as a file; import on another device; the corpus never touches a server.

**Project:** `pocket-rag` — Q&A over a corpus you choose (your notes, a manual, your module handbook), with the ten-question evaluation table in the post.

### <span style="color:#2980B9">Week 5 — Agents on the Device</span>

**Goal:** a model that calls tools you wrote, inside the browser, to do something you actually needed.

1. **Tool calling with a small model.** Load `LFM2.5-2.6B-ONNX` if your Week 0 benchmark says the device can carry it, else stay on 1.2B. Define two tools as JSON schema; parse the call; return the result; loop. Liquid trained the 2.6B for exactly this; the 1.2B will be worse, and seeing that is part of the week.
2. **Browser tools.** `fetch` to a public JSON API, `localStorage`/IndexedDB as memory, the clock, geolocation (with consent), the Week 4 retriever as a tool.
3. **Loops and stop conditions.** Max steps, a confirm-before-side-effect gate, and a log panel that shows every call and result. The doom-loop failure shape from Week 1 reappears here; the student must catch it.
4. **Evaluate an agent.** Five tasks, pass/fail, steps taken, tokens spent. Compare 1.2B and 2.6B on the same five if both run.
5. **Where the big models still win.** Honest session: what the agent couldn't do, and what an API-backed version would cost per run. Students who also took BWAI bring their Week 5 numbers.

**Project:** an agent page that automates one real thing in your week (a reading-list triager, a price watcher over a public API, a note-filer), deployed, with the five-task table and the call log in the post.

### <span style="color:#2980B9">Week 6 — Portfolio & What's Next</span>

Same structure as BWAI Week 6: tidy the five deployed pages into a portfolio site on GitHub Pages, write the reflective piece, review three peers. One added section in the write-up: *my device's limits* — the benchmark numbers, the biggest model it ran, and the one project it couldn't carry.

---

## <span style="color:#16A085">5. What is deliberately not in the track</span>

- **Decision models (d1).** No ONNX or WebGPU build found; Python/llama.cpp only. A single optional Week 3 aside shows the idea with a local `llama-server`; not a session.
- **Fine-tuning.** Out of scope for six weeks. Pointed to in Week 6 reading.
- **Audio.** `LFM2.5-Audio-1.5B-ONNX` exists and is WebGPU-tagged; parked for a possible Week 3 alternative after launch, once someone has run it on a phone.
- **Native apps.** Liquid's LEAP SDK is deprecated and they now point at llama.cpp directly; a PWA covers the course's needs.

---

## <span style="color:#16A085">6. The CPU lane</span>

For a student whose device fails the Week 0 floor. Same six weeks, same projects, with the model served by `llama-server` from a GGUF build in the Codespace and the page talking to it over the forwarded port. The student loses "runs on my phone" and keeps everything else. <span style="color:#C0392B">Not yet measured:</span> tokens/s for `LFM2.5-350M` and `1.2B` GGUF on a 2-core Codespace. If the 1.2B is unusable there, the lane runs on 350M throughout and the Week 5 agent uses 350M with the gap stated.

---

## <span style="color:#16A085">7. CLI additions (brief for a later commit)</span>

- `bwai webgpu-check` — serves `tools/webgpu-check/index.html` on a forwarded port; the page reports the adapter, loads `LFM2.5-350M-ONNX`, runs one prompt, prints tokens/s, and offers a one-click *copy for Anseo* of the result.
- `bwai new-page NAME --week N` — scaffolds `projects/weekN/NAME/` with `index.html`, `app.js` (loader + chat template + streamer + cost meter), `manifest.json`, `sw.js`, and a README; `--vision` swaps in the VL loader.
- `bwai pages-deploy` — pushes the current project to the student's `gh-pages` branch and prints the URL; `bwai submit` posts it to Anseo as today.

`verify.py` for this track drops the Anthropic check and adds a Node/npm check.

---

## <span style="color:#16A085">8. Before launch — the open items</span>

| item | why it matters | how to close it |
|---|---|---|
| Device floor | whole track depends on it | Week 0 page on Lava, S22 Ultra, one weak machine; record tokens/s |
| 350M, Thinking and 2.6B browser download sizes | students on metered connections | read the three model cards' file listings; add to §2 |
| Browser embedder for Week 4 | no Liquid ONNX embedding export found | pick one with a licence compatible with CC BY-SA course material; or Liquid ships one |
| Codespace CPU lane speed | fallback viability | `llama-server` + 350M/1.2B GGUF on a 2-core Codespace |
| LFM Open License full text | redistribution of weights is not planned (students download from the Hub), but confirm nothing in the licence touches teaching use | read it once; note the section |
| Track name | Irish name, cleared | Ainm check on the shortlist |

---

## <span style="color:#16A085">9. Sources (fetched 2026-10-17)</span>

- Liquid AI model library and licensing summary: https://www.liquid.ai/models · https://www.liquid.ai/pricing
- LFM2.5-1.2B-Instruct-ONNX card (transformers.js snippet, Q4/FP16 sizes, WebGPU notes): https://huggingface.co/LiquidAI/LFM2.5-1.2B-Instruct-ONNX
- LFM2.5-VL-450M-ONNX card (dtype map, ~770 MB, `AutoModelForImageTextToText`): https://huggingface.co/LiquidAI/LFM2.5-VL-450M-ONNX
- LiquidAI ONNX exports on the Hub (350M, 1.2B-Thinking, 2.6B, Audio-1.5B, VL-1.6B/3B): https://huggingface.co/LiquidAI
- Liquid WebGPU Spaces (1.2B-Thinking, 2.6B, VL-450M/1.6B/3B): https://huggingface.co/spaces/LiquidAI
- LFM2.5-2.6B agentic training and tool-use benchmarks: https://www.liquid.ai/blog/lfm2-5-2-6b
- LEAP SDK deprecation: https://docs.liquid.ai/deployment/on-device/sdk/overview
