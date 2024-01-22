import csv

from brute_force_evaluation import brute_force
from plane_sweep_evaluation import sweep_plane
import data_generation


def main():
    for num in range(10, 2000, 10):
        t_brute_force = 0
        t_sweep_plane = 0
        for i in range(0, 5):
            data_generation.data_generate(x_range=(1, num * 10), y_range=(1, num * 10), length_min=num*0.5, length_max=num*5, m=num, n=num)
            t_brute_force += brute_force()
            t_sweep_plane += sweep_plane()
        with open('time_static_05_5.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow((num, t_brute_force, t_sweep_plane))
        print(f'Finish segment size: {num}')


if __name__ == "__main__":
    main()
