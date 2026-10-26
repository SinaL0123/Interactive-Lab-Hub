# Lab 5 — On-device observation

**Student:** Sina Liu
**Platform:** Raspberry Pi 5, USB webcam, Raspberry Pi Connect

For this lab, I set up an on-device observation pipeline: YOLO detects people from a webcam, an interpreter turns detections into short readings, and Qwen summarizes the resulting log. All inference ran locally on the Raspberry Pi.

## Part A — Set up on-device AI

I created a Python virtual environment, installed the Lab 5 requirements, exported `yolo26n` to NCNN for Raspberry Pi inference, and tested the model on an internet image and a webcam photo.

### YOLO tests

The NCNN model identified people and a bus in the provided test image.

![YOLO detection of people and a bus](media/yolo-bus-result.jpg)

I then captured a webcam image using `snap.py` and ran the same model. It detected one person with 0.90 confidence.

![YOLO detection on my webcam image](media/yolo-snap-result.png)

### Ollama models

I installed the two local Qwen models required for the lab: `qwen3.5:0.8b` for image and text understanding, and `qwen3:0.6b` for faster text-only responses.

![Ollama models installed on the Pi](media/ollama-models.png)

## Part B — Real-time person detection with YOLO

I ran `yolo_person.py` through Raspberry Pi Connect and tested the detector while moving into and out of frame, standing near and far from the camera, and showing different numbers of people. The detector drew boxes and confidence scores around each detected person.

![Live YOLO detection of three people](media/yolo-live-detection.png)

I also tested the headless mode, which prints the x-position, height, confidence, and number of detected people without opening a display window.

![Headless YOLO output](media/yolo-headless-output.png)

### Experiment recordings

| Recording | Command | What I tested |
| --- | --- | --- |
| [1](media/yolo-experiment-1.mp4) | `python yolo_person.py` | Baseline live person detection while moving close to, away from, and across the camera. |
| [2](media/yolo-experiment-2.mp4) | `python yolo_person.py --conf 0.2` | A lower confidence threshold, including a phone image with people in its background. |
| [3](media/yolo-experiment-3.mp4) | `python yolo_person.py --conf 0.7` | A higher confidence threshold and the difference between strong and weak detections. |
| [4](media/yolo-experiment-4.mp4) | `python yolo_person.py --headless` | The terminal-only output used when no display window is available. |

### Limits and errors I observed

1. In the baseline recording, moving extremely close to the camera left only a blurred, partial body in the frame. The detector could miss that view or draw a less stable box because there was not enough visible body shape for a reliable classification.
2. With `--conf 0.2`, the lowered threshold accepted weak detections. When I held up a phone image, YOLO also labeled the people inside the phone image/background as `person`, including low-confidence boxes around 0.20–0.39. This is a false positive for a system that needs to count physical people in the room.
3. With `--conf 0.7`, only stronger detections survived, so uncertain people were more likely to disappear. The phone itself was also recognized as a separate object in the experiment. This shows the tradeoff: a higher threshold reduces weak false positives but can hide real people, while object labels still depend on the visual context.

## Part C — Hand pose with MediaPipe

I ran `hand_pose.py` with the webcam. MediaPipe detected the 21 landmarks of my hand. The distance between my thumb and index finger controlled a percentage value; the screenshot below shows the value at 37%.

![MediaPipe hand landmarks and pinch-based percentage control](media/mediapipe-pinch.png)

I then tested the gesture controls. Pinching my thumb and index finger adjusted the value from 0% to 84%. With the Quiet Coyote pose—index finger and pinky extended, middle and ring fingers folded, and thumb held against them—the program displayed `quiet coyote!` and set the value to 0%.

#### Pinch at 0%

![Pinch test at zero percent](media/hand-pose-pinch-0-percent.png)

#### Pinch at 84%

![Pinch test at 84 percent](media/hand-pose-pinch-84-percent.png)

#### Quiet Coyote at 0%

![Quiet Coyote gesture detected](media/mediapipe-quiet-coyote.png)

For an overnight interaction, this gesture could act as the hand-off ritual before bed: it mutes the device and starts the overnight observation mode. The morning report could require a second deliberate gesture before it is shown.

## Part D — Qwen reasoning on the Pi

I used `ask_qwen.py` to send my webcam image to the local `qwen3.5:0.8b` model with the question: **“What is in this photo?”** The model described a person in a workshop/studio setting and completed the request in 58.6 seconds.

![Qwen image analysis running locally on the Pi](media/qwen-image-analysis.png)

### Three text questions

I also asked the local `qwen3.5:0.8b` model three text questions:

| Question | Response summary | Time |
| --- | --- | --- |
| “When is Chinese Lunar New Year 2027?” | It answered “February 12, 2028,” which does not answer the requested year and is an example of the small model producing an incorrect factual response. | 10.4 s |
| “What is the color of rose?” | “The color of a rose is red.” | 1.6 s |
| “How to make a unagi don?” | It gave a short cooking procedure, but incorrectly suggested boiling the fish before slicing and frying it. | 8.0 s |

![Three local Qwen questions, answers, and timings](media/qwen-three-questions.png)

The answers show why an observant device should keep the model's task narrow and verify important claims against its input data rather than treating every answer as ground truth.

### Model comparison

I repeated the Lunar New Year question using `qwen3:0.6b`. The two small local models took almost the same amount of time, but neither response gave a reliable Gregorian date.

| Model | Result | Time |
| --- | --- | --- |
| `qwen3.5:0.8b` | Said Lunar New Year 2027 would be February 12, 2028, which is the wrong year. | 10.4 s |
| `qwen3:0.6b` | Gave a lunar-month description and incorrectly equated it with New Year's Day. | 10.3 s |

![The same Lunar New Year question run with qwen3 0.6b](media/qwen-0.6b-comparison.png)

This comparison was only 0.1 seconds faster with the smaller model, and accuracy did not improve. For factual questions, a local model's answer should be checked against a reliable source before it is used in an interactive system.

## Part E — YOLO to Qwen pipeline

I ran `yolo_to_qwen.py` for 61 seconds. The script converted YOLO detections into time-stamped readings such as `1 person(s) at center/close`, saved 25 lines to `watch_log.txt`, and sent the log to Qwen for a summary.

Qwen reported that two people were initially near the center of the frame, that one later moved left/far, and that no new people appeared or disappeared during the observation interval. This result also shows a limitation: the summary is only as reliable as the detector log, so changes in camera framing and detector confidence can affect its account.

![YOLO-to-Qwen log and local Qwen summary](media/yolo-qwen-pipeline.png)

## Reflection

This lab helped me understand how the whole pipeline connects. YOLO first turns what the camera sees into boxes, then the script turns those boxes into short text readings, and Qwen only sees that text log rather than the original video. I was surprised that the live person detection still worked reasonably well on the Pi, while asking Qwen about an image took much longer.

The tests also made the limitations feel very clear. Changing the confidence threshold could either create extra detections or make a real person disappear, and Qwen gave wrong answers to some simple factual questions. I also realized that small choices in `interpret()`—for example, what counts as left, center, close, or far—change the story that Qwen receives. If I build this into an overnight project, I would need to keep the camera framing stable and treat the final AI summary as a helpful interpretation, not as unquestionable truth.

## Contributions

I performed the Raspberry Pi setup, webcam experiments, recordings, and on-device model runs. I used ChatGPT/Codex to troubleshoot installation issues and organize this documentation.

# Lab 5 Part 2: Overnight Sensation

For Part 2, you will use the observant system from Part 1 to design a night-time interaction. On-device AI is slow, so let it work while you sleep. The person meets the device twice: **before bed**, when they hand the night over, and **when awake**, when the device gives something back. In between, the pipeline from Part E runs on its own.

Two flavors, pick one or mix them:

* **Sense all night.** The Pi watches, listens or measures from bedtime until morning and keeps a log.
* **Process all night.** You already have the data (a day of phone photos, a long recording) and the Pi needs hours to get through it.

Two house rules. Sample rather than stream: one look every 5 to 30 seconds is plenty, and it keeps the Pi cool. And keep everything on the Pi: tell the people you live with, point the camera at things rather than at beds, and delete the snapshots after the demo.

## Part F. 
### Read Part 2 and storyboard your night-time interaction

Storyboard a night-time interaction built on your observant system, in three panels:

1. **Before bed.** How does the person hand the night over, and how does the device acknowledge it?
2. **While asleep.** What does the device watch or work through?
3. **When awake.** What is the one thing the person learns, and in what medium?

Stuck? A kitchen that tells you who raided the fridge. A desk that reports whether you actually went to bed. A window that names the quietest hour. A plant that describes its night. Find something better.

Use storyboards and/or [Verplank diagrams](https://ccrma.stanford.edu/courses/250a-fall-2004/IDSketchbok.pdf).

\*\*\***Insert ideas, sketches, Verplank diagrams and storyboards for your night-time interaction here.**\*\*\*

## Prep for Part 2

1. Look at and give feedback on the Part F storyboards.
   **Put the feedback for your ideas here.**
2. [Update your Lab Hub](prep.md#get-the-latest-content) to get the latest content for Part 2.
3. Decide where the device will spend the night and who else lives there. Get their OK before the first run.
4. Revise your storyboard with the feedback and with what you learned in Part E about where the pipeline breaks.

\*\*\***Post your revised storyboard here.**\*\*\*

## Part G. 
### Design the interaction before

The hand-off: the person tells the device what to watch tonight, and the device acknowledges it. Keep it to a thirty-second ritual. A button or a touch (Lab 4), a spoken sentence (Lab 3), a wave or a Quiet Coyote at the camera (Part C). The acknowledgement can be a line on the display, a tone, or an LED that dims rather than lights up. At its simplest, the hand-off just sets the question that the morning will answer.

\*\*\***Describe the interaction before.**\*\*\*

## Part H. 
### Incorporate the observant system

The Part E pipeline becomes the night shift. `overnight.py` runs your `interpret()` from `yolo_to_qwen.py` every few seconds, people only unless you pass `--all`, and writes the readings to `night_log.jsonl`; the reasoning waits for the morning. Start it inside `tmux` so it keeps running after you close your laptop, and stop it with Ctrl-C in the morning:

```
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ tmux new -s night
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ python overnight.py
```

Fake a night first: run it for thirty seconds while you walk around, stop it, and run `morning.py` from Part I. When that looks right, run a real night. If your storyboard needs a sensor rather than the camera, swap in the Lab 4 example code and log its reading the same way.

\*\*\***Screenshots or videos of the running system.**\*\*\*

## Part I. 
### Design the interaction after

The reveal. The night produced a log; the morning turns it into something a half-awake person can take in. `morning.py` is the smallest version: it asks Qwen for a three-sentence report.

```
(.venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 5 $ python morning.py
```

Make it yours: show the report on the Mini PiTFT, read it aloud with Piper from Lab 3, plot the night as a timeline, or ask for JSON (`--json`, Part D) and move a servo. Whatever you pick, make sure it is honest about a night in which nothing happened.

## Final documentation

Document all the prototypes and iterations you have designed and worked on. The deliverables for this lab are writings, sketches, photos, and videos that show what your system:

* "Looks like": how the device sits in the room at night, and what it looks like at bedtime and in the morning.
* "Works like": the pipeline from detector to interpreter to log to reasoner, with a real night's data.
* "Acts like": how a person hands the night over and what they get back.

\*\*\***Include a short video of the whole system**\*\*\*

As always, make sure you document contributions and ideas from others (and AI) explicitly in your writeup.

You are permitted (but not required) to work in groups and share a turn in; you are expected to make equal contribution on any group work you do, and N people's group project should look like N times the work of a single person's lab. Make sure the page for the group turn in is linked to your personal Interactive Lab Hub page.

## Deliverables & Submission for Lab 5

For submission, the readme.md page for this lab should be edited to include the work you have done:
* Upload any materials that explain what you did, including your code and night log, into your Lab 5 repository, and link them in your Lab 5 readme.md.
* Labs are due on Sundays, make sure to submit your Lab 5 readme.md to Canvas.

<details>
  <summary><strong>Submission Cleanup Reminder (Click to Expand)</strong></summary>

  **Before submitting your README.md:**
  - This readme.md file has a lot of extra text for guidance.
  - Remove all instructional text and example prompts from this file.
  - You may either delete these sections or use the toggle/hide feature in VS Code to collapse them for a cleaner look.
  - Your final submission should be neat, focused on your own work, and easy to read for grading.
</details>
