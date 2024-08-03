# Stardust

![image](https://elite.bbcelite.com/images/general/Elite-Tube.png)

This is a nostalgic project. Aspects of the [1984 Elite game](https://en.wikipedia.org/wiki/Elite_(video_game)) is implemented in Python.

Specifically, when you run `python stardust.py`, you will be traveling through a void at some speed, but you will see:

https://github.com/user-attachments/assets/1164476d-30c3-4156-a629-1d1399ac849f

- Small particles of dust (or star dusts) out there in space which give rise to the immersive feeling that we are flying through space.
- All 4 views Front, Rear, Left, Right, use KEYS `1`, `2`, `3`, and `4` respectively.
- Roll, Pitch, and Speed adjustments.
  - Speed up: `SPACE`, Slow down: `/`
  - Roll Left: `,` (`<`) Roll Right: `.` (`>`)
  - Climb: `x`  Bank: `s`

Implementation is based on information from the [Fully documented source code for Elite on the BBC Micro and NES](https://elite.bbcelite.com/) by [Mark Moxon](https://www.markmoxon.com/).

The project uses pygame.

# Note
Set `$ export OPENBLAS_NUM_THREADS=1` to avoid [high CPU usage from numpy](https://github.com/numpy/numpy/issues/26096). 