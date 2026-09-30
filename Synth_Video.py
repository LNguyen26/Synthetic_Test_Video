import numpy as np


#20 s still, 10 s at 4 px/frame, 20 s still, 10 s at 40 px/frame
#assume 30fps?


H, W = 400, 600          # canvas
a, b = 46, 74            # half-axes: a along x, b along y
y, x = np.ogrid[:H, :W]
FPS = 30


def change(A, B):
    XOR = (A ^ B).sum() #number of pixels that changed
    area = (A.sum() + B.sum()) / 2 #average area of the two ellipses
    overlap = (A & B).sum() #number of pixels that overlap
    d_form1 = XOR / area #density of changed pixels
    d_form2 = 2 * (1 - overlap / area) #density of changed pixels, alternative formula
    assert abs(d_form1 - d_form2) < 1e-12    #tolerance for floating point error
    return d_form1




def hold(pos, secs): #when the ellipse is still
    return [pos] * (secs * FPS)


def sweep(pos, step, secs): #when the ellipse is moving
    out = []
    for _ in range(secs * FPS):
        if pos + step > W - a - 3: #if the ellipse is about to go out of bounds, reverse dir w 2 px of headroom
            step = -step
        elif pos + step < a + 2: #does the oppsite if it goes the other way w 2 px of headroom
            step = -step
        pos += step
        out.append(pos)
    return out


sched  = hold(300, 20) #initial position 20s
sched += sweep(sched[-1],  4, 10) #4px 10s
sched += hold(sched[-1], 20) #hold 20s still
sched += sweep(sched[-1], 40, 10) #40px 10s
#sched is a list that holds all the positions of the ellipse for each frame


def mask(cx):
    return ((x - cx)/a)**2 + ((y - H//2)/b)**2 <= 1 #ellipse, doesn't have cy bc it only moves horizontally


BG_L, FISH_L = 180, 60

def render(m):
    return np.where(m, FISH_L, BG_L).astype(np.uint8) #returns a 2D array of the image, with the mask applied
#depends on true/false (puts the mask into a brightness image)


def chained_loop(masks):
    #builds each frame once, holds it in prev, measures against next frame, then moves on to the next frame
    areas = []
    prev = None #initializes prev frame as nothing (bc the prev of the first frame is nothing)
    d_list = []
    for cur in masks:
        assert cur.dtype == bool
        areas.append(cur.sum())
        if prev is not None:
            d_list.append(change(prev, cur)) #change between frames
        prev = cur
    assert len(d_list) == len(masks) - 1
    return np.array(d_list), np.array(areas)

#next: have two masks: one true and one estimated from grayscale, compare them to each other