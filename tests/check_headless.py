# Headless check, run with mayapy from the repo root:
#   /Applications/Autodesk/maya2026/Maya.app/Contents/bin/mayapy tests/check_headless.py
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import maya.standalone
maya.standalone.initialize()
import maya.cmds as cmds
import set_dresser as sd

def positions():
    out = []
    for grp in ("rocks", "trees"):
        for c in cmds.listRelatives(grp, children=True) or []:
            p = cmds.xform(c, q=True, ws=True, t=True)
            out.append((grp, round(p[0], 4), round(p[2], 4)))
    return out

cmds.file(new=True, force=True)
cmds.undoInfo(state=True, infinity=True)
cmds.sphere(n="someone_elses_rock")  # must survive clear
sd.build_ground()
r, t = sd.scatter(rocks=30, trees=12, seed=12)
pts = positions()
print("placed", r, "rocks,", t, "trees")
assert (r, t) == (30, 12)
assert len(cmds.listRelatives("rocks", c=True)) == 30 and len(cmds.listRelatives("trees", c=True)) == 12
bad = [p for p in pts if not sd.is_clear(p[1], p[2])]
assert not bad, bad
assert all(abs(p[1]) >= 3.0 for p in pts), "path margin"
print("min |x|:", min(abs(p[1]) for p in pts))

cmds.undo()
assert not cmds.objExists("rocks") and not cmds.objExists("trees"), "one undo"
assert cmds.objExists("ground"), "undo removed only the scatter"
cmds.redo()
assert len(cmds.listRelatives("rocks", c=True)) == 30
print("one undo removes the scatter, redo brings it back")

sd.clear()
assert cmds.objExists("someone_elses_rock") and cmds.objExists("ground")
sd.scatter(30, 12, seed=12); again = positions(); sd.clear()
sd.scatter(30, 12, seed=13); other = positions(); sd.clear()
assert again == pts, "seed 12 repeat"
assert other != pts, "seed 13 differs"
print("seed 12 repeats exactly, seed 13 differs")
sd.clear()  # warns: nothing to clear
print("ALL CHECKS PASSED")
