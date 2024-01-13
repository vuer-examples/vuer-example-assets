if __name__ == "__main__":

    import asyncio
    from pathlib import Path

    import numpy as np
    import open3d as o3d

    from vuer import Vuer, VuerSession
    from vuer.events import Set, ClientEvent
    from vuer.schemas import DefaultScene, TriMesh, PointCloud, TimelineControls

    mesh = o3d.io.read_triangle_mesh("stairs.ply")
    vertices = np.asarray(mesh.vertices)
    faces = np.asarray(mesh.triangles)

    app = Vuer()

    @app.spawn(start=True)
    async def main(proxy: VuerSession):
        proxy.set @ DefaultScene()

        await asyncio.sleep(0.0)

        proxy.upsert @ [
            PointCloud(key="infill", vertices=vertices, position=[0, 0, 0], color="red", size=0.025),
        ]

        while True:
            await asyncio.sleep(1.0)
