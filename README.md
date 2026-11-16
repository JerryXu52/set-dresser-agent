# Set Dresser

A Maya tool that dresses a set. It scatters rocks and trees across a 40×40 ground,
and keeps them off a path (4 units wide, along Z through the middle, with a 1-unit
margin on each side) and out of a round pond (radius 6, centred at x=10, z=10).

A window gives you sliders for rock count, tree count, area and seed, a checkbox to
keep the path and pond clear, and **Scatter** and **Clear** buttons. If you use the
same seed and settings, you get the same set every time.

Built for the *Trees & Rocks* tutorial (HSG-5232 Programming for Animators, SVA MFA Computer Arts).

## Requirements

- Maya 2026 (2027 also works). Python 3 and `maya.cmds` only. No PyMEL.

## Install

Copy `set_dresser.py` and `set_dresser_ui.py` into your Maya scripts folder. To find
the folder, run this in the Script Editor:

```python
import maya.cmds as cmds; print(cmds.internalVar(userScriptDir=True))
```

## Run

In the Script Editor's Python tab:

```python
import set_dresser_ui
set_dresser_ui.show()
```

Or, with no window:

```python
import set_dresser
set_dresser.build_ground()
set_dresser.scatter(rocks=30, trees=12, seed=12)
```

## Files

| File | What it is |
|---|---|
| `set_dresser.py` | The engine: settings at the top, `make_rock`, `make_tree`, the `is_clear` rule, `scatter`, `clear`. It has no UI. |
| `set_dresser_ui.py` | The window. It reads the controls and calls the engine, nothing more. |
| `send_to_maya.py` | Sends one line of Python to a Maya that has opened port 7001. |
| `tests/check_headless.py` | A check that runs in `mayapy`, with no Maya window open. |
| `CLAUDE.md` | The rules file the agent worked from. |
| `BRIEF.md` | The brief, the plan, and the change requests sent to the agent. |

## Behaviour

- Everything a scatter makes goes into a `rocks` group or a `trees` group. **Clear**
  deletes those two groups and nothing else. The ground, path and pond stay.
- One scatter is one undo step.
- If the area is too small to fit the counts, Maya shows one warning line.

## Check it without opening Maya

```sh
/Applications/Autodesk/maya2026/Maya.app/Contents/bin/mayapy tests/check_headless.py
```

The check confirms these things:

- It places exactly 30 rocks and 12 trees.
- Nothing lands on the path, its margin, or the pond.
- One undo removes the whole scatter.
- **Clear** leaves other objects alone.
- Seed 12 repeats exactly, and seed 13 gives a different set.
