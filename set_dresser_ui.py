# set_dresser_ui.py — the window. It reads controls and calls the engine.
#
#   import set_dresser_ui
#   set_dresser_ui.show()

import maya.cmds as cmds

import set_dresser

WIN = "setDresserWin"
SIZE = (420, 330)


def _settings():
    """Read every control. The window's only job besides calling the engine."""
    return dict(
        rocks=cmds.intSliderGrp("sdRocks", q=True, v=True),
        trees=cmds.intSliderGrp("sdTrees", q=True, v=True),
        area=cmds.floatSliderGrp("sdArea", q=True, v=True),
        keep_clear=cmds.checkBox("sdKeepClear", q=True, v=True),
        seed=cmds.intSliderGrp("sdSeed", q=True, v=True),
    )


def on_scatter(*_):
    set_dresser.build_ground()
    set_dresser.scatter(**_settings())


def on_clear(*_):
    set_dresser.clear()


def show():
    if cmds.window(WIN, exists=True):
        cmds.deleteUI(WIN)

    cmds.window(WIN, title="Set Dresser", widthHeight=SIZE)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=6, columnOffset=("both", 10))

    cmds.frameLayout(label="How many", marginWidth=6, marginHeight=6)
    cmds.intSliderGrp("sdRocks", label="Rocks", field=True, min=0, max=200, value=30)
    cmds.intSliderGrp("sdTrees", label="Trees", field=True, min=0, max=60, value=12)
    cmds.setParent("..")

    cmds.frameLayout(label="Where", marginWidth=6, marginHeight=6)
    cmds.floatSliderGrp("sdArea", label="Area", field=True, min=4.0, max=20.0,
                        value=set_dresser.AREA)
    cmds.checkBox("sdKeepClear", label="Keep the path and pond clear", value=True)
    cmds.intSliderGrp("sdSeed", label="Seed", field=True, min=0, max=999,
                      fieldMaxValue=999999, value=12)
    cmds.setParent("..")

    cmds.separator(height=8, style="none")
    cmds.button(label="Scatter", height=36, command=on_scatter)
    cmds.button(label="Clear", command=on_clear)

    cmds.showWindow(WIN)
    # Maya remembers a window's size by name. Set it after showing, or the old size wins.
    cmds.window(WIN, e=True, widthHeight=SIZE)
