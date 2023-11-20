# read the input horizontal segments
hor_seg_num = int(input().split()[2])

hor_segs = []

for _ in range(hor_seg_num):
    line = input()
    values = list(map(int, line.split()))
    hor_segs.append(values)

# read the input vertical segments
ver_seg_num = int(input().split()[2])

ver_segs = []

for _ in range(ver_seg_num):
    line = input()
    values = list(map(int, line.split()))
    ver_segs.append(values)


def is_intersect(hor_seg, ver_seg):
    a, a_, b = hor_seg
    c, d, d_ = ver_seg
    return a <= c <= a_ and d <= b <= d_


res = 0

for hor_seg in hor_segs:
    for ver_seg in ver_segs:
        if is_intersect(hor_seg, ver_seg):
            res = res + 1

print(res)