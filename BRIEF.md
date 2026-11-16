# The brief and the conversation

## Brief

> Build me a set-dressing tool for Maya, in this folder, following CLAUDE.md.
>
> What it does: scatters rocks and trees across a 40x40 ground plane and keeps
> them off a path (4 wide, along Z through the middle) and out of a round pond
> (radius 6 at x=10, z=10). A window with sliders for rock count, tree count
> and area, a checkbox for keeping the path and pond clear, a Scatter button
> and a Clear button.
>
> Who uses it: a set dresser who will never open the code.
>
> What it has to get right: one function per thing it makes, one function
> for the rules, everything it makes under a group per kind, Clear deletes
> only those groups, one scatter is one undo, the window only reads controls
> and calls the engine.
>
> Tell me your plan before you touch anything.

## Plan (written by the agent before building)

1. Two files. `set_dresser.py` is the engine and has no UI. `set_dresser_ui.py` is the window.
2. Settings at the top of the engine: ground size, area, path half-width, pond centre and radius, and a cap on tries.
3. `make_rock(x, z, size)` and `make_tree(x, z, height)` each make one thing and return its name. `paint` makes one shader per kind and reuses it.
4. `is_clear(x, z)` holds every placement rule.
5. `scatter_rocks` and `scatter_trees` each use a `while` loop with a tries cap. They place into the `rocks` and `trees` groups through `group_for`.
6. `scatter()` wraps both in one undo chunk (`try/finally`).
7. `clear()` deletes only the `rocks` and `trees` groups, and shows `cmds.warning` if there was nothing to clear.
8. `build_ground()` makes the ground, path and pond, and skips any that already exist.
9. The window has sliders and a checkbox, and its Scatter and Clear buttons call the engine.

Plan check against CLAUDE.md: two files ✓, make_rock/make_tree ✓, is_clear ✓, groups ✓, undo chunk ✓.

## Change 1: path margin

> In is_clear: keep everything at least 1 unit back from the path's edges,
> not just off the path. Make the 1 a setting at the top of the file, next to
> the path's width, not a number inside the function.

Result: a new `PATH_MARGIN = 1.0` setting next to `PATH_HALF_WIDTH`, and `is_clear`
now tests `abs(x) < PATH_HALF_WIDTH + PATH_MARGIN`. The headless check found the
smallest |x| to be 3.15, so nothing landed within 3 units of the path's centre line.

## Change 2: seed

> Add a Seed slider to the window. The same seed with the same settings must
> produce the same set every time, so a director can say "seed 12 was the one".
> Use random.seed. Show me the two lines that make it work.

The two lines, at the top of `scatter()`:

```python
if seed is not None:
    random.seed(seed)
```

Python's random numbers are seeded before anything random happens, so every
`uniform()` call after that comes out in the same order. Verified headless:
seed 12 → identical positions twice; seed 13 → different.
