# <span style="color:#1F3A5F">BWAI Local — Week 0: Launch Pad</span>

<span style="color:#7F8C8D">**Time required:** 45–60 minutes (most of it is one download)
**Complete before:** Session 1
**Goal:** a language model has generated text on your own hardware, you know how fast, and you've met your cohort.</span>

---

## <span style="color:#16A085">How this track works</span>

Each week has **five sessions** (30–45 minutes each) and a **weekly project**. Sessions build on each other — Session 3 assumes you've done Sessions 1 and 2 — but you work through them at your own pace within the week.

The one fixed point is the **weekly project deadline (Sunday)**. That's when you share your work on Anseo and peer review starts.

**Time commitment: ~5 hours per week.**

**What's different from the Claude track.** Nothing you build here calls an API. Every project is a web page that downloads a model into your browser once and then runs it on your own GPU. That means no API key, no bill, and no server. It also means the model is small — between 350 million and 2.6 billion parameters — and you are going to watch it fail. That is the point: by Week 6 you will know, from your own evidence, what a small local model can and cannot do.

**Miss a week?** Rejoin the next one. The Anseo posts and peer projects are the record of what you missed.

---

## <span style="color:#16A085">What you need before you start</span>

You should be comfortable with:

- Writing and running Python (the course tooling is Python)
- **Basic JavaScript** — variables, functions, `async`/`await`, editing an HTML file. The pages you build are JavaScript. If `await fetch(url)` means nothing to you, spend an hour on it first.
- Git (commit, push, pull, branch)
- A terminal

**You also need a device that can run the model.** This is the one hard requirement the Claude track doesn't have:

- A laptop or desktop with a GPU of any kind (integrated is fine) **and** Chrome or Edge, current version, **or**
- A recent Android phone with Chrome.

Step 3 tests your device. If it fails, the **CPU lane** (Step 7) keeps you in the course.

**You do NOT need:**

- An Anthropic account or any API key
- A Railway account
- Any AI or ML experience
- A discrete graphics card — but the better your GPU, the bigger the model you can carry

---

## <span style="color:#16A085">Step 1: Create your accounts</span>

Two accounts. That's it.

### GitHub
[github.com](https://github.com). Use a professional username — it becomes part of your portfolio. Students: apply for the [GitHub Student Developer Pack](https://education.github.com/pack) for free Codespaces hours.

### Anseo
[anseo.irish](https://anseo.irish). Create your account and join the **BWAI Local** course community. This is where you share work, get help, and review peers. It's not a side channel.

---

## <span style="color:#16A085">Step 2: Open the course Codespace</span>

We use **GitHub Codespaces** for editing, Git, and serving your pages. The model itself never runs in the Codespace — it runs in your browser on your device. The Codespace is just the workbench.

1. Go to the course repository: `github.com/[COURSE_ORG]/bwai`
2. Click **Code → Codespaces → Create codespace on main**
3. Wait 2–3 minutes the first time

You get VS Code in your browser with a terminal at the bottom.

### Connect to Anseo (optional for Week 0, needed by Week 1)

Anseo → **Settings → API Tokens → Generate Token**, name it `bwai course CLI`, copy it. Add it as a Codespace secret at [github.com/settings/codespaces](https://github.com/settings/codespaces): name `ANSEO_API_TOKEN`, value the token, repository access: this repo. Or put it in `.env`:

```
ANSEO_URL=https://anseo.irish
ANSEO_API_TOKEN=anseo_your_token_here
```

---

## <span style="color:#16A085">Step 3: Test your device</span>

This is the step that matters. In the Codespace terminal:

```bash
cd tools/webgpu-check
python -m http.server 8000
```

VS Code will pop up a **Ports** notification. Click **Open in Browser**. If no notification appears, open the **Ports** tab at the bottom, find port 8000, and click the globe icon.

**Open that URL on the device you will use for the course.** If that's your phone, click the globe icon's *copy* button instead, make the port **Public** (right-click the port → Port Visibility → Public), and send the link to your phone.

The page runs three checks:

**Check 1 — WebGPU.** It asks the browser for a GPU adapter and prints its name and limits. If this fails:

- **Chrome/Edge on desktop:** go to `chrome://flags/#enable-unsafe-webgpu`, set it to *Enabled*, restart the browser. Then check `chrome://gpu` and look for *WebGPU: Hardware accelerated*.
- **Android Chrome:** should work on recent phones with no flag. If it doesn't, update Chrome.
- **Safari / Firefox:** use Chrome or Edge for this course. WebGPU support in other browsers varies and we don't test against it.

**Check 2 — Download.** Click **Load model**. The page downloads `LFM2.5-350M-ONNX` at Q4 precision — **about 276 MB**, once. The browser caches it, so later loads are instant. Do this on Wi-Fi.

**Check 3 — Generate.** Click **Run benchmark**. The page sends one fixed question to the model and shows the answer streaming in, then prints:

- **Time to first token** (how long before the model started answering)
- **Tokens per second** (how fast it kept going)
- **Total tokens** and **wall time**

Click **Copy for Anseo**. It copies a one-line result like:

```
LFM2.5-350M Q4 · Apple M2 (WebGPU) · TTFT 0.41 s · 38.2 tok/s · 142 tokens · Chrome 142
```

**Reading the number.** The track's rule of thumb:

| tokens/s on 350M | what it means |
|---|---|
| above 20 | comfortable; try the 1.2B model in Week 1 |
| 8–20 | usable; 1.2B will be slow, stay on 350M for the first weeks |
| below 8 | take the CPU lane (Step 7) — or find a better device |

These thresholds are a starting point set before launch, not measured on a range of devices. The *Benchmarks* thread will show whether they're right.

---

## <span style="color:#16A085">Step 4: Post your benchmark</span>

Paste the copied line into the **Benchmarks** thread on Anseo, with your device model if the page didn't detect it (phones often report only "Adreno" or "Mali"). This thread is the course's own hardware table. Read what others posted — you'll see the spread between a phone and a gaming laptop, and that spread is Week 1's subject.

---

## <span style="color:#16A085">Step 5: Scaffold your first page</span>

In the Codespace terminal, from the repo root:

```bash
mkdir -p projects/week1-thinking-small/hello-local
cp tools/webgpu-check/index.html projects/week1-thinking-small/hello-local/index.html
```

(When the `bwai new-page` command lands, it does this with a cleaner template. For Week 0 the check page is the template.)

Open the new `index.html`. Find this line near the top of the script:

```js
const PROMPT = "In one sentence, what is the most important thing for a developer to understand about working with a small on-device language model?";
```

Change the prompt to anything you like. Serve the folder:

```bash
cd projects/week1-thinking-small/hello-local
python -m http.server 8000
```

Reload the page on your device. The model is already cached, so it loads in a second or two. Run it. That's your first on-device inference from a page you edited.

Commit and push:

```bash
git add projects/week1-thinking-small/hello-local
git commit -m "Week 0: hello-local"
git push
```

---

## <span style="color:#16A085">Step 6: Introduce yourself on Anseo</span>

In the **Introductions** thread:

- Your name or handle
- What you do right now
- The device you'll use for the course and your tokens/s
- One thing you want to be able to build that runs with no server

Reply to at least one other introduction.

---

## <span style="color:#16A085">Step 7: The CPU lane</span>

If Check 1 fails on every device you have, or Check 3 comes in under 8 tokens/s, you do the course on the CPU lane. Same six weeks, same projects; the model runs in the Codespace instead of your browser, and your page talks to it over the forwarded port.

In the Codespace:

```bash
pip install llama-cpp-python[server]
python -m llama_cpp.server --hf_model_repo_id LiquidAI/LFM2.5-350M-GGUF --model '*q4_0.gguf' --port 8080
```

This serves an OpenAI-compatible endpoint at `http://localhost:8080/v1`. The Week 2 pocket chat has a switch for it.

**Known unknowns for this lane**, stated plainly: the course author has not yet measured tokens/s for the 350M or 1.2B GGUF on a 2-core Codespace, and the exact GGUF filename pattern in `LiquidAI/LFM2.5-350M-GGUF` must be checked against that repo's file list before you rely on the glob above. Post in the Week 0 help thread if the command fails and we'll fix the doc.

What you lose on this lane: "runs on my phone." What you keep: everything else.

---

## <span style="color:#16A085">What you don't need to do</span>

- **Don't install Node or npm.** The pages load `@huggingface/transformers` from a CDN as an ES module. No bundler, no build step.
- **Don't install Python locally.** Codespaces has it.
- **Don't deploy yet.** GitHub Pages deployment starts in Week 1.
- **Don't download the 1.2B model yet.** It's ~1.2 GB; Week 1 Session 1 does it deliberately.
- **Don't read ahead.**

---

## <span style="color:#16A085">If something goes wrong</span>

1. **The page says "WebGPU not available."** Follow the Check 1 fixes above. On a desktop, `chrome://gpu` tells you exactly what the browser thinks of your GPU.
2. **The download stalls.** It's a 276 MB file from huggingface.co. Check the browser's Network tab; a corporate or college network may block the host. Try a phone on mobile data to confirm, then take the CPU lane if the block is permanent.
3. **"Load model" works but "Run benchmark" throws.** Open DevTools (F12) → Console and copy the full red text into the Week 0 help thread. Include your Check 1 output.
4. **Everything works but it's very slow.** That's a result, not a failure. Post it. Then read Step 7.
5. **Restart the Codespace.** GitHub menu → Codespaces → Stop → Restart. Fixes most mysteries.

---

## <span style="color:#16A085">Checklist</span>

- [ ] GitHub account created
- [ ] Anseo account created, joined BWAI Local
- [ ] Anseo API token generated (optional)
- [ ] Codespace opens
- [ ] Check page: WebGPU adapter detected on my course device
- [ ] Check page: 350M model downloaded and cached
- [ ] Check page: benchmark ran; I have a tokens/s number
- [ ] Benchmark line posted in the Anseo *Benchmarks* thread
- [ ] hello-local page edited, run, committed, pushed
- [ ] Introduction posted; replied to one peer
- [ ] If my device failed: CPU lane endpoint running

All ticked: see you in Session 1.

---

## <span style="color:#16A085">8. Author's notes (not for students)</span>

- `tools/webgpu-check/index.html` was written against the transformers.js snippet on Liquid's `LFM2.5-1.2B-Instruct-ONNX` card (`AutoModelForCausalLM`, `device: "webgpu"`, `dtype: "q4"`), pointed at the 350M export. The 350M card itself shows a lower-level `onnxruntime-web` loop rather than the high-level API; the high-level call is expected to work for the same `lfm2` architecture but <span style="color:#C0392B">has not yet been run in a browser</span>. First thing to do before any student sees this: open the page on Lava and the S22 Ultra and fix what breaks.
- The CDN import pins `@huggingface/transformers@4.3.1`, the version jsDelivr listed on 2026-10-17. Bump deliberately, not automatically.
- The 276 MB figure is from the 350M-ONNX card's variants table (Q4). FP16 is ~692 MB; Q8 is not supported on WebGPU.
- The tokens/s thresholds in Step 3 are placeholders in the honest sense: a first guess, labelled as such on the page and in the doc, to be replaced by the Benchmarks thread's data after the first cohort.
- Model licence: LFM Open License v1.0 (`lfm1.0`). Students download from the Hub directly; the course redistributes no weights.
