import json
import math
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

TRACKS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tracks'))


def load_track(filename):
    path = os.path.join(TRACKS_DIR, filename)
    print("Loading from:", path)
    with open(path, 'r') as f:
        return json.load(f)



def draw_track(track_data):
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_title(track_data['name'])

    for segment in track_data['segments']:
        label = segment['meta'].get('section', '')

        if segment['type'] == 'straight':
            x0, y0 = segment['start']
            x1, y1 = segment['end']
            ax.plot([x0, x1], [y0, y1], 'k-')

            # Label the middle of the line
            mid_x = (x0 + x1) / 2
            mid_y = (y0 + y1) / 2
            ax.text(mid_x, mid_y, label, fontsize=8, ha='center', va='center')

        elif segment['type'] == 'corner':
            center = segment['center']
            radius = segment['radius']
            theta1 = segment['start_angle']
            theta2 = segment['end_angle']

            # Draw arc
            arc = Arc(
                center,
                width=2 * radius,
                height=2 * radius,
                angle=0,
                theta1=theta1,
                theta2=theta2,
                color='blue'
            )
            ax.add_patch(arc)

            # Label the arc at approx midpoint angle
            mid_angle = math.radians((theta1 + theta2) / 2)
            label_x = center[0] + radius * math.cos(mid_angle)
            label_y = center[1] + radius * math.sin(mid_angle)
            ax.text(label_x, label_y, label, fontsize=8, ha='center', va='center')

    ax.axis('off')
    plt.show()


if __name__ == '__main__':
    track = load_track('indianapolis_oval.json')
    draw_track(track)