import tkinter as tk
from tkinter import Scale
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import hsv_to_rgb


class CircleBisectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Circle Bisection GUI")

        # Create the main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create a matplotlib figure
        self.figure, self.axs = plt.subplots(1, 2, figsize=(10, 5))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.main_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        # Create a slider to adjust the line position
        self.slider = Scale(self.root, from_=-1.0, to=1.0, resolution=0.01,
                            orient=tk.HORIZONTAL, label="Line Position", command=self.update_plot)
        self.slider.pack(fill=tk.X)

        # Initialize the plot
        self.update_plot(0)

    def update_plot(self, value):
        # Clear the axes
        for ax in self.axs:
            ax.clear()

        # Circle parameters
        radius = 1
        theta = np.linspace(0, 2 * np.pi, 1000)
        x_circle = radius * np.cos(theta)
        y_circle = radius * np.sin(theta)

        # Line position from slider
        line_pos = float(value)

        # Set a default RGB color for the line (red as a placeholder)
        rgb_color = (1, 0, 0)
        hue_angle = 0  # Default hue angle when no rind pieces are rendered

        # Check if the line is at the middle
        if not np.isclose(line_pos, 0, atol=1e-5):
            # Determine which side is smaller
            left_mask = x_circle < line_pos
            right_mask = ~left_mask

            if line_pos < 0:
                # Smaller piece on the left
                x_bisect = x_circle[left_mask]
                y_bisect = y_circle[left_mask]
            else:
                # Smaller piece on the right
                x_bisect = x_circle[right_mask]
                y_bisect = y_circle[right_mask]

            # Scale down the bisected piece
            x_piece = 0.45 * x_bisect
            y_piece = 0.45 * y_bisect

            # Calculate the angular span of the piece
            span_angle = np.arctan2(y_piece[-1], x_piece[-1]) - np.arctan2(y_piece[0], x_piece[0])
            span_angle = span_angle if span_angle > 0 else span_angle + 2 * np.pi  # Ensure positive span

            # Determine the hue angle
            hue_angle = np.degrees(span_angle) % 360
            hue = hue_angle / 360  # Normalize hue to [0, 1]
            rgb_color = hsv_to_rgb((hue, 1, 1))  # Convert hue to RGB

            # Duplicate the piece and arrange rind-to-rind
            num_pieces = max(1, int(2 * np.pi / span_angle))
            angles = np.linspace(0, 2 * np.pi, num_pieces, endpoint=False)

            for angle in angles:
                cos_a, sin_a = np.cos(angle), np.sin(angle)

                # Rotate the rind piece
                x_rotated = cos_a * x_piece - sin_a * y_piece
                y_rotated = sin_a * x_piece + cos_a * y_piece

                # Connect the ends to close the piece
                x_rotated = np.append(x_rotated, x_rotated[0])
                y_rotated = np.append(y_rotated, y_rotated[0])

                # Draw the rind segments (color-coded)
                self.axs[1].plot(x_rotated, y_rotated, color=rgb_color, linewidth=1.5)

                # Add line segments for connections
                for i in range(len(x_rotated) - 1):
                    self.axs[1].plot([x_rotated[i], x_rotated[i + 1]],
                                     [y_rotated[i], y_rotated[i + 1]],
                                     color=rgb_color, linestyle='-', linewidth=0.8)

            # Ensure aspect ratio and title for the rind plot
            self.axs[1].set_aspect('equal')
            self.axs[1].set_title("Reduced Pieces Forming Circle")

        # First subplot: Original circle with line
        self.axs[0].plot(x_circle, y_circle, label="Original Circle")
        self.axs[0].axvline(x=line_pos, color=rgb_color, linestyle="--", linewidth=2,
                            label=f"Hue Line ({hue_angle:.1f}°)")
        self.axs[0].text(line_pos, 1.05, f"Hue: {hue_angle:.1f}°", color=rgb_color, fontsize=10, ha='center')
        self.axs[0].set_aspect('equal')
        self.axs[0].set_title("Circle with Adjustable Line")
        self.axs[0].legend()

        # Draw the canvas
        self.canvas.draw()


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = CircleBisectionApp(root)
    root.mainloop()

input('Press ENTER to exit')
