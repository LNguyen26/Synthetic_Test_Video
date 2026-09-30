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