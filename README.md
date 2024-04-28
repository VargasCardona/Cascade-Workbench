
![LogoWorkbench](https://github.com/VargasCardona/Computer-Vision-Workbench/assets/142677238/6e32dd0a-1428-49ad-a68a-918eeb6b5678)

# Cascade Workbench

Minimalistic graphical interface that enables the user to visualize and fine-tune Haar Cascade models for object detection tasks. 

## Features

- Visualization of Haar Cascade models.
- Media input supported.
- Webcam input supported.


## Preview

![Demo](https://github.com/VargasCardona/Computer-Vision-Workbench/assets/142677238/81309cb5-e418-4ff9-a6b8-4f04760441f1)


## Roadmap

- Integrate a Haar Cascade trainer


## Optimizations

Multithreading to avoid interrupting the graphical user interface while frames get processed.

## Directory Struture

```
├─ LICENSE
├─ README.md
├─ datasets
│  ├─ neg
│  │  └─ yoru.jpg
│  └─ pos
│     └─ yoru.jpg
├─ exceptions
│  ├─ __init__.py
│  ├─ __pycache__
│  │  ├─ __init__.cpython-311.pyc
│  │  └─ exceptions.cpython-311.pyc
│  └─ exceptions.py
├─ main.py
├─ media
│  └─ haar.png
├─ models
│  ├─ __init__.py
│  ├─ __pycache__
│  │  └─ __init__.cpython-310.pyc
│  ├─ eve.xml
│  └─ frontalface_default.xml
├─ src
│  ├─ __init__.py
│  ├─ __pycache__
│  │  ├─ __init__.cpython-310.pyc
│  │  ├─ __init__.cpython-311.pyc
│  │  ├─ gui.cpython-310.pyc
│  │  ├─ gui.cpython-311.pyc
│  │  ├─ vision.cpython-310.pyc
│  │  └─ vision.cpython-311.pyc
│  ├─ example.py
│  ├─ gui.py
│  ├─ quick_trainer.py
│  ├─ training.py
│  └─ vision.py
└─ workbench_run.bat
```
> [!NOTE]  
> The `models/` and `media/` directory contain some basic Haar Cascade models and media for quick testing.

## Tech Stack

**Languages:** Python

**Libraries:** OpenCV, DearPyGui.


## License

[GPL-3.0](https://www.gnu.org/licenses/)

