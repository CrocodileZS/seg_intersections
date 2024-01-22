import random
import matplotlib.pyplot as plt

# # Constants for the range of values
# X_RANGE = (1, 100)
# Y_RANGE = (1, 100)
# SEGMENT_LENGTH_MIN = 10
# SEGMENT_LENGTH_MAX = 30
# NUM_HORIZONTAL = 20
# NUM_VERTICAL = 20


# Function to generate non-overlapping horizontal segments
def generate_horizontal_segments(num_segments, x_range, y_range, length_min, length_max):
    segments = []
    used_y = set()
    while len(segments) < num_segments:
        y = random.randint(*y_range)
        if y not in used_y:
            x1 = random.randint(*x_range)
            x2 = x1 + random.randint(length_min, length_max)
            segments.append((x1, x2, y))
            used_y.add(y)
    return segments


# Function to generate non-overlapping vertical segments
def generate_vertical_segments(num_segments, x_range, y_range, length_min, length_max):
    segments = []
    used_x = set()
    while len(segments) < num_segments:
        x = random.randint(*x_range)
        if x not in used_x:
            y1 = random.randint(*y_range)
            y2 = y1 + random.randint(length_min, length_max)
            segments.append((x, y1, y2))
            used_x.add(x)
    return segments


def data_generate(x_range, y_range, length_min, length_max, m, n):
    # Generate the segments
    horizontal_segments = generate_horizontal_segments(m, x_range, y_range, length_min, length_max)
    vertical_segments = generate_vertical_segments(n, x_range, y_range, length_min, length_max)

    # # Plotting the segments
    # plt.figure(figsize=(10, 10))
    #
    # # Plot horizontal segments
    # for x1, x2, y in horizontal_segments:
    #     plt.plot([x1, x2], [y, y], 'b')
    #
    # # Plot vertical segments
    # for x, y1, y2 in vertical_segments:
    #     plt.plot([x, x], [y1, y2], 'r')
    #
    # # Setting the axes limits
    # plt.xlim(0, x_range[1])
    # plt.ylim(0, y_range[1])
    #
    # # Show the plot
    # plt.show()

    # After generating the line segments and ensuring there are no overlaps within each set,
    # we now format the dataset as text.

    # Generate the text representation of the dataset
    horizontal_text = "\n".join(f"{x1} {x2} {y}" for x1, x2, y in horizontal_segments)
    vertical_text = "\n".join(f"{x} {y1} {y2}" for x, y1, y2 in vertical_segments)

    # Combine horizontal and vertical segments text
    dataset_text = f"horizontal segments {m}\n{horizontal_text}\nvertical segments {n}\n{vertical_text}"

    # Save dataset text to a .txt file
    file_path = 'dataset.txt'
    with open(file_path, 'w') as file:
        file.write(dataset_text)


if __name__ == "__main__":
    data_generate((1, 100), (1, 100), 10, 30, 20, 20)

