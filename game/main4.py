import asyncio
import pyray as r

async def main():
    r.init_window(400,300,"d");x=y=0
    while not r.window_should_close():
        x+=1;y+=1
        if x>400:x=0
        if y>300:y=0
        r.begin_drawing()
        r.clear_background(r.BLACK)
        r.draw_rectangle_rounded(r.Rectangle(int(x), int(y), 40, 40), 0.1, 10, r.RED)
        # r.draw_rectangle_rounded_lines_ex(r.Rectangle(int(x), int(y), 40, 40), 0.1, 10, 2, r.RED) # Changing to this line causes error in pygbag

        r.end_drawing()
        await asyncio.sleep(0)
    r.close_window()

asyncio.run(main())

# compile with:
# python -m pygbag --template noctx.tmpl --PYBUILD 3.12 --ume_block 0 --git .
