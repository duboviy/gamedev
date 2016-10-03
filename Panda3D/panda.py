# -*- coding: utf-8 -*-
from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3


class PandaGameApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        # Disable the camera trackball controls.
        self.disableMouse()
        # Add the spinCameraTask procedure to the task manager.
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        self.configure_environ()
        self.confige_actor()

    def configure_environ(self):
        # Load the environment model.
        self.environ = self.loader.loadModel("models/environment")
        # Reparent the model to render.
        self.environ.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.environ.setScale(0.25, 0.25, 0.25)
        self.environ.setPos(-8, 42, 0)

    def confige_actor(self):
        # Load and transform the panda actor.
        self.pandaActor = Actor("models/panda-model",
                                {"walk": "models/panda-walk4"})
        self.pandaActor.setScale(0.005, 0.005, 0.005)
        self.pandaActor.reparentTo(self.render)
        # Loop its animation.
        self.pandaActor.loop("walk")

        # Create the four lerp intervals needed for the panda to
        # walk back and forth.
        PosInterval1 = self.pandaActor.posInterval(3, Point3(0, -10, 0),
                                                   startPos=Point3(0, 10, 0))
        PosInterval2 = self.pandaActor.posInterval(3, Point3(0, 10, 0),
                                                   startPos=Point3(0, -10, 0))
        HprInterval1 = self.pandaActor.hprInterval(1, Point3(180, 0, 0),
                                                   startHpr=Point3(0, 0, 0))
        HprInterval2 = self.pandaActor.hprInterval(1, Point3(0, 0, 0),
                                                   startHpr=Point3(180, 0, 0))

        # Create and play the sequence that coordinates the intervals.
        self.pandaPace = Sequence(PosInterval1,
                                  HprInterval1,
                                  PosInterval2,
                                  HprInterval2,
                                  name="pandaPace")
        self.pandaPace.loop()

    # Define a procedure to move the camera.
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont


if __name__ == "__main__":
    app = PandaGameApp()
    app.run()
