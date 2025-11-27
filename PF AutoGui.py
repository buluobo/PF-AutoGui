import time
from tkinter import Tk, IntVar, messagebox
from tkinter.ttk import Button, Scale
import pynput


class Win(Tk):
    def __init__(self):
        super().__init__()
        self.event_player = EventPlayer()
        # 组件
        self.record_button = self.__record_button()  # 录制按钮
        self.stop_button = self.__stop_button()  # 停止按钮
        self.play_button = self.__play_button()  # 播放按钮
        self.scale_num = IntVar(value=1)  # 播放次数变量
        self.num_scale = self.__num_scale()  # 播放次数滑动条
        self.num_button = self.__num_button()  # 播放次数重置按钮
        # 界面布局
        self.__ui()  # 界面
        self.__layout__()  # 布局
        self.__bind()  # 绑定

    def __ui(self):
        # 主界面设置
        self.title("PF AutoGui")
        width = 260
        height = 130
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        self.geometry(
            f"{width}x{height}+{screenwidth-width-50}+{(screenheight - height)//2-200}")
        self.resizable(0, 0)
        self.attributes('-alpha', 0.9)
        self.attributes('-topmost', True)

    def __layout__(self):
        self.record_button.place(x=20, y=20, width=60, height=30)
        self.stop_button.place(x=100, y=20, width=60, height=30)
        self.play_button.place(x=180, y=20, width=60, height=30)
        self.num_scale.place(x=20, y=60, width=220, height=18)
        self.num_button.place(x=110, y=85, width=40, height=26)

    def __bind(self):
        self.record_button.config(command=self.record)
        self.stop_button.config(command=self.stop)
        self.play_button.config(command=self.play)

    def __record_button(self):
        return Button(self, text="录制")

    def __stop_button(self):
        return Button(self, text="停止")

    def __play_button(self):
        return Button(self, text="播放")

    def __num_scale(self):
        return Scale(self, from_=1, to=100, variable=self.scale_num, command=self.__set_scale)

    def __num_button(self):
        return Button(self, textvariable=self.scale_num, command=lambda: self.scale_num.set(1))

    def __set_scale(self, event):
        self.scale_num.set(int(self.scale_num.get()))

    def record(self):
        # 开始录制
        messagebox.showinfo("提示", "录制开始")
        self.play_button.config(state="disabled")
        self.event_player.events.clear()
        self.event_player.listen()

    def stop(self):
        if self.event_player.events:
            # 停止录制
            if self.event_player.keyboard_listener:
                self.event_player.keyboard_listener.stop()
            if self.event_player.mouse_listener:
                self.event_player.mouse_listener.stop()
            messagebox.showinfo("提示", "录制结束")
            self.play_button.config(state="normal")

    def play(self):
        # 播放录制
        if self.event_player.events:
            messagebox.showinfo("提示", "播放开始")
            self.record_button.config(state="disabled")
            self.stop_button.config(state="disabled")
            self.update()
            for _ in range(self.scale_num.get()):
                self.event_player.play()
                self.scale_num.set(self.scale_num.get() - 1)
                self.update()
            messagebox.showinfo("提示", "播放结束")
            self.scale_num.set(1)
            self.record_button.config(state="normal")
            self.stop_button.config(state="normal")


class EventPlayer:
    def __init__(self):
        # 事件列表
        self.events = []

    def listen(self):
        self.keyboard_listener = pynput.keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        self.mouse_listener = pynput.mouse.Listener(
            on_click=self.on_click,
            on_scroll=self.on_scroll,
            on_move=self.on_move
        )
        self.keyboard_listener.start()
        self.mouse_listener.start()

    def play(self):
        for index, event in enumerate(self.events):
            if event['type'] == 'key_press':
                pynput.keyboard.Controller().press(event['key'])
            elif event['type'] == 'key_release':
                pynput.keyboard.Controller().release(event['key'])
            elif event['type'] == 'mouse_click':
                if event['pressed']:
                    pynput.mouse.Controller().press(event['button'])
                else:
                    pynput.mouse.Controller().release(event['button'])
            elif event['type'] == 'mouse_scroll':
                pynput.mouse.Controller().scroll(event['dx'], event['dy'])
            elif event['type'] == 'mouse_move':
                pynput.mouse.Controller().position = event['position']
            if index + 1 < len(self.events):
                time.sleep(self.events[index + 1]['time'] - event['time'])
            else:
                time.sleep(0.5)

    def on_press(self, key):
        event = {
            'type': 'key_press',
            'key': key,
            'time': time.time()
        }
        self.events.append(event)

    def on_release(self, key):
        event = {
            'type': 'key_release',
            'key': key,
            'time': time.time()
        }
        self.events.append(event)

    def on_click(self, x, y, button, pressed):
        event = {
            'type': 'mouse_click',
            'button': button,
            'pressed': pressed,
            'position': (x, y),
            'time': time.time()
        }
        self.events.append(event)

    def on_scroll(self, x, y, dx, dy):
        event = {
            'type': 'mouse_scroll',
            'position': (x, y),
            'dx': dx,
            'dy': dy,
            'time': time.time()
        }
        self.events.append(event)

    def on_move(self, x, y):
        event = {
            'type': 'mouse_move',
            'position': (x, y),
            'time': time.time()
        }
        self.events.append(event)


if __name__ == "__main__":
    win = Win()
    win.mainloop()
