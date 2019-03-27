# Rigs of Rods - Blender addon

This project intends to expand recently created (and excellent) [Ulteq's import/export scripts](https://github.com/RigsOfRods/rigs-of-rods/tree/master/tools/blender) and add interactive editing capabilities.

Also, RoR ecosystem contains a solid amount of discontinued Python code, which deserves to be studied and re-used:
 * [RoRToolkit](https://github.com/only-a-ptr/ror-toolkit) - Standalone wxPython + OGRE 1.8 application focused on editing terrain (legacy .terrn format) but also capable of editing vehicles
 * [BlenderPortable 2.49 with plugins](https://archives.rigsofrods.net/old-forum-mybb/thread-126.html) - Vehicle parsing + editing capabilities.

Target Blender version is 2.8 (currently beta with unstable Python API) because it's remade UI is much more intuitive and accessible to casual user,
and since this project intends to add it's own (elaborate) UI, it makes sense to adopt Blender 2.8 early to avoid learning it twice.
