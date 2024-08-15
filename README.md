# Manim Contour Animator
Implements a DFS-like algorithm to generate Manim code that programatically animates the edges of an image. Uses Canny edge detection from the OpenCV package.

See example renderings here: https://www.youtube.com/playlist?list=PLj1SweGV2RLRSbV_7_Y9ZpZWi91RY7bsj

# Usage
`threshold-tester.py` can be used to test different threshold values for the Canny edge detection to determine the desired image to be animated. `converter.py` produces an output Python file (`out.py`) that contains the Manim code for the video. `draw.bat`/`draw.sh` runs the Manim code to render the video.

# Notes
`converter.py` uses an optimized version of the algorithm that removes node points in areas resembling straight lines to reduce the rendering time for the Manim output. `converter-old.py` is the original version of the algorithm that does not perform such optimizations, which may result in longer rendering times but greater detail.