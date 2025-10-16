
# Playing 3D Movie in VisionPro

This example shows how to use background images + layers
to play a 3D movie in the VisionPro.

Before you start, first run the following script:

```shell
# From the Mary Project: https://www.meryproject.com/
# 360 Stereo from http://pedrofe.com/rendering-for-oculus-rift-with-arnold/
wget -O mary.webm https://threejs.org/examples/textures/MaryOculus.webm
```

![Side view of the 3D movie screen](figures/20_3D_movie.png)

The underlying rendering engine supported a layer binary bitmask
for both objects and the camera. Below we set the two image planes,
left and right, to `layers=1` and `layers=2`. Note that these two 
masks are associated with left eye's camera and the right eye's
camera.

```{admonition} ImagePlane.layer Property
Pay attention to the layer property. You can set it to 3 to have
it show up in both eyes! layers=0 is the default, and it appears 
on all of the cameras.
```


```python
from asyncio import sleep

import imageio as iio
from tqdm import tqdm

from vuer import Vuer
from vuer.events import ClientEvent
from vuer.schemas import ImageBackground

reader = iio.get_reader("./mary.webm")

app = Vuer()


# we add the handler here because the spawn(start=True) binding is blocking.
@app.add_handler("CAMERA_MOVE")
async def on_camera(event: ClientEvent, session):
    assert event == "CAMERA_MOVE", "the event type should be correct"
    print("camera event", event.etype, event.value)


@app.spawn(start=True)
async def show_heatmap(session):
    # session.set @ Scene()
    # session.upsert @ Hands()
    # session.upsert @ Movable(position=[1, 1, -1], key="movable")
    # session.set @ Scene(bgChildren=[
    #     Hands(),
    #     PointLight(),
    # ])

    frames = [f for f in reader]

    while True:
        for i, frame in tqdm(enumerate(frames), desc="playing video"):
            # use the upsert(..., to="bgChildren") syntax, so it is in global frame.
            session.upsert(
                [
                    ImageBackground(
                        # We slice the left side of the stereo video
                        # frame[::2, 152:720 + 152, :],
                        frame[::, :1024, :],
                        aspect=1.42,
                        height=0.4,
                        distanceToCamera=0.4,
                        layers=1,
                        # One of ['b64png', 'png', 'b64jpeg', 'jpeg']
                        format="jpeg",
                        quality=10,
                        key="background-left",
                        interpolate=True,
                        fixed=True,
                        position=[0, 0.5, -1],
                        alphaSrc="http://localhost:8012/static/vinette.jpg"
                    ),
                    ImageBackground(
                        # We slice the right side of the stereo video
                        # frame[::2, 1024 + 152: 1024 + 152 + 720, :],
                        frame[::, 1024:, :],
                        aspect=1.42,
                        height=0.4,
                        distanceToCamera=0.4,
                        layers=2,
                        # One of ['b64png', 'png', 'b64jpeg', 'jpeg']
                        format="jpeg",
                        quality=10,
                        key="background-right",
                        interpolate=True,
                        fixed=True,
                        position=[0, 0.5, -1],
                        alphaSrc="http://localhost:8012/static/vinette.jpg"
                    ),
                ],
                to="bgChildren",
            )
            # 'jpeg' encoding should give you about 30 fps with a 16ms wait in -between.
            await sleep(0.02)
```
