# Interactive-Python-Mandelbrot
A clickable interactive mandelbrot set, made with Python 3, PIL, and Tkinter. Uses multiprocessing, colour palette is randomly generated.

## Usage
1. Install required modules with `pip install -r requirements.txt`.
2. Run the program with `python3 framework.py`
3. Left-click the image where you want to zoom in
4. Right-click the image to zoom out
5. Control+left-click to shift the view to that point
6. Control+right-click to change the image colour-palette
6. Middle-click to save the image

## Commandline options
    -h, --help               Command-line help dialogue.
    -i, --iterations         Number of iterations done for each pixel. Higher is more accurate but slower.
    -x                       The x-center coordinate of the frame.
    -y                       The y-center coordinate of the frame.
    -m, --magnification      The magnification level of the frame. Scientific notation (e.g. 3E-4) is permitted.
    -wi, --width             The number of pixels wide the image is.
    -he, --height            The number of pixels high the image is.
    -s, --save               Flag to save the generated image.
    -nm, --noMulti           Flag to not use multiprocessing.

## Mandelbrot Set feature rendered by this program
<img src="https://raw.githubusercontent.com/rosslh/Interactive-Python-Mandelbrot/master/pictures/image.png" width="100%">
