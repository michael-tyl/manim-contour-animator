import numpy as np
import cv2 as cv
from collections import deque

out_name = "out-old.py"
blur = 5

def init_file():
    with open(out_name, "w") as out:
        with open("template.txt", "r") as template:
            out.write(template.read())
    
def end_file():
    with open(out_name, "a") as out:
        with open("end_template.txt", "r") as template:
            out.write(template.read())

if __name__ == "__main__":
    init_file()

    # Read in image (gray-scale)
    img = cv.imread("image.jpg",0)
    img = cv.GaussianBlur(img,(blur,blur), sigmaX=0, sigmaY=0) 
    edges = cv.Canny(img,50,100,L2gradient=True)

    # Make visited arrays
    visited = np.full((len(edges),len(edges[0])), False)
    visited2 = np.full((len(edges),len(edges[0])), False)

    # Define order of pixel checking (starts by looking up and goes counterclockwise)
    dx = [0,1,1,1,0,-1,-1,-1]
    dy = [-1,-1,0,1,1,1,0,-1]

    # Determine length of axes (makes sure image is not stretched)
    x_len = 14
    y_len = 8
    px_per_unit = max(len(edges) / y_len, len(edges[0]) / x_len)
    x_len = len(edges[0]) / px_per_unit
    y_len = len(edges) / px_per_unit

    # Write coordinate axes
    with open(out_name, "a") as out:
        out.write(f"""
    ax = Axes(
            x_range=[0,{len(edges[0])},1],
            y_range=[0,{len(edges)},1],
            x_length={x_len},
            y_length={y_len}
        )
    return [""")
    
    edge_count = 0

    # Loop through every pixel
    for y in range(len(edges)):
        for x in range(len(edges[0])):
            # Check if visited already
            if visited[y][x]:
                continue

            # Continue if pixel is empty
            if not edges[y][x]:
                continue
            
            # Make a list of current pixels on the edge
            # y comes first to have top-most coordinates first when sorted
            # Negative x to have right-most coordinates first when sorted
            cur_px = [(y,-x)]

            # Search through all connected full pixels
            stack = deque()
            stack.append((x,y))

            while len(stack):
                cur_x, cur_y = stack.pop()

                visited2[cur_y][cur_x] = True

                # Check neighboring pixels in order
                for i in range(8):
                    nx = cur_x + dx[i]
                    ny = cur_y + dy[i]
                    if not (nx >= 0 and nx < len(edges[0]) and ny >= 0 and ny < len(edges)):
                        continue
                    if visited[ny][nx] or visited2[ny][nx] or not edges[ny][nx]:
                        continue

                    visited2[ny][nx] = True

                    # Add next pixel to stack and list
                    stack.append((nx,ny))
                    cur_px.append((ny,-nx))

            # Go through pixels again, keeping track of order
            first_px = (-cur_px[len(cur_px)-1][1],cur_px[len(cur_px)-1][0])
            stack.append(first_px)
            x_list = []
            y_list = []

            edge_count += 1

            while len(stack):
                cur_x, cur_y = stack.pop()
                x_list.append(cur_x)
                y_list.append(len(edges) - cur_y)

                # Check neighboring pixels in order
                for i in range(8):
                    nx = cur_x + dx[i]
                    ny = cur_y + dy[i]
                    if not (nx >= 0 and nx < len(edges[0]) and ny >= 0 and ny < len(edges)):
                        continue
                    if visited[ny][nx] or not edges[ny][nx]:
                        continue
                    
                    visited[ny][nx] = True
                    visited2[ny][nx] = True

                    # Add next pixel to the stack
                    stack.append((nx,ny))

                    # Break loop - only consider one pixel after another (no branching)
                    break
            
            # Write to file
            if len(x_list) > 1:
                with open(out_name, "a") as out:
                    out.write(f"""
            Create(ax.plot_line_graph(x_values={x_list},
            y_values={y_list},
            line_color=WHITE,stroke_width=weight,add_vertex_dots=False)),""")

    end_file()
