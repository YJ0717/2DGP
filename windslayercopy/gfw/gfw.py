from pico2d import *
import time

_running = True
_stack = []

def start(scene):
    import gfw
    open_canvas(1250, 720, sync=True) #--- 캔버스 크기 설정
    push(scene)

    global frame_time
    last_time = time.time()

    while _running:
        now = time.time()
        gfw.frame_time = now - last_time
        last_time = now

        _stack[-1].world.update()
        clear_canvas()
        _stack[-1].world.draw()
        update_canvas()

        for e in get_events():
            handled = _stack[-1].handle_event(e)
            if not handled:
                if e.type == SDL_QUIT:
                    quit()
                elif e.type == SDL_KEYDOWN and e.key == SDLK_ESCAPE:
                    pop()

    while _stack:
        _stack.pop().exit()

    close_canvas()

def start_main_module():
    import sys
    scene = sys.modules['__main__']
    start(scene)

def change(scene):
    if _stack:
        _stack.pop().exit()
    _stack.append(scene)
    scene.enter()

def push(scene):
    if _stack:
        _stack[-1].pause()
    _stack.append(scene)
    scene.enter()

def pop():
    _stack.pop().exit()
    if not _stack:
        quit()
        return
    _stack[-1].resume()

def quit():
    global _running
    _running = False

def top():
    return _stack[-1]
