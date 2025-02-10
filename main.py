from tkinter import *
from tkinter import messagebox

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
check_marks = ""
timer = ""
is_timer_running = False
STATS_FILE = "pomodoro_stats.json"

# ---------------------------- PomodoroTimer ------------------------------- #
class PomodoroTimer:
    def __init__(self):
        self.reset_button = None
        self.timer_text = None
        self.canvas = None
        self.pause_button = None
        self.check_label = None
        self.timer_label = None
        self.start_button = None
        self.window = Tk()
        self.window.title("Pomodoro Timer")
        self.window.config(padx=100, pady=50, bg=YELLOW)

        self.reps = 0
        self.check_marks = ""
        self.timer = None
        self.paused = False
        self.is_timer_running = False  # 新增：跟踪计时器状态
        self.current_count = 0

        self.setup_ui()
# ---------------------------- TIMER RESET ------------------------------- #
    def reset_timer(self):
        if self.timer:
            self.window.after_cancel(self.timer)
        self.canvas.itemconfig(self.timer_text, text="00:00")
        self.timer_label.config(text="Timer")
        self.check_label.config(text="")
        self.reps = 0
        self.check_marks = ""
        self.paused = False
        self.is_timer_running = False
        self.start_button.config(state=NORMAL)  # 重新启用开始按钮
        self.pause_button.config(state=DISABLED)  # 禁用暂停按钮
    # ---------------------------- TIMER PAUSE ------------------------------- #
    def pause_timer(self):
        if self.timer:
            self.window.after_cancel(self.timer)
            self.paused = True
            self.start_button.config(state=NORMAL)  # 重新启用开始按钮
            self.pause_button.config(state=DISABLED)  # 禁用暂停按钮
# ---------------------------- TIMER MECHANISM ------------------------------- #
    def start_timer(self):
        # 检查计时器是否已经在运行
        if self.is_timer_running and not self.paused:
            return
        if self.paused:
            self.paused = False
            self.is_timer_running = True
            self.start_button.config(state=DISABLED)  # 禁用开始按钮
            self.pause_button.config(state=NORMAL)  # 启用暂停按钮
            self.count_down(self.current_count)
            return

        self.is_timer_running = True
        self.start_button.config(state=DISABLED)  # 禁用开始按钮
        self.pause_button.config(state=NORMAL)  # 启用暂停按钮

        self.reps += 1
        work_sec = WORK_MIN * 60
        short_break_sec = SHORT_BREAK_MIN * 60
        long_break_sec = LONG_BREAK_MIN * 60

        if self.reps % 8 == 0:
            self.count_down(long_break_sec)
            self.timer_label.config(text="Break", fg=RED)
        elif self.reps % 2 == 0:
            self.count_down(short_break_sec)
            self.timer_label.config(text="Break", fg=PINK)
        else:
            self.count_down(work_sec)
            self.timer_label.config(text="Work", fg=GREEN)

    def timer_complete(self):
        """处理计时器完成时的所有操作"""
        self.is_timer_running = False
        self.check_marks += "✔" if self.reps % 2 == 0 else ""
        self.check_label.config(text=self.check_marks)
        # 设置一个很短的延迟来显示消息框，确保00:00已经显示
        self.window.after(100, lambda: messagebox.showinfo("Pomodoro",
                                                           "Time's up! Take a break!" if self.reps % 2 == 1 else "Break is over! Time to work!"))
        # 更新按钮状态
        self.start_button.config(state=NORMAL)
        self.pause_button.config(state=DISABLED)
        self.window.update()
# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
    def count_down(self, count):
        self.current_count = count
        count_min = count // 60
        count_sec = count % 60

        self.canvas.itemconfig(self.timer_text, text=f"{count_min:02d}:{count_sec:02d}")

        if count > 0 and not self.paused:
            self.timer = self.window.after(1000, self.count_down, count - 1)
        elif count <= 0:
            self.timer_complete()
    # ---------------------------- UI ------------------------------- #
    def setup_ui(self):
        #label
        self.timer_label = Label(text="Timer", font=(FONT_NAME, 50),bg=YELLOW, fg=GREEN)
        self.timer_label.grid(column=1, row=0)

        self.check_label = Label(text="", bg=YELLOW, fg=GREEN)
        self.check_label.grid(column=1, row=3)

        # Canvas
        self.canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
        tomato_img = PhotoImage(file="tomato.png")
        self.canvas.create_image(100, 112, image=tomato_img)
        self.canvas.image = tomato_img  # Keep a reference
        self.timer_text = self.canvas.create_text(100, 130, text="00:00", font=(FONT_NAME, 35, "bold"), fill="white")
        self.canvas.grid(column=1, row=1)

        # Buttons
        self.start_button = Button(text="Start", bg=YELLOW, highlightthickness=0, borderwidth=0, command=self.start_timer)
        self.start_button.grid(column=0, row=4)

        self.pause_button = Button(text="Pause", bg=YELLOW, highlightthickness=0, borderwidth=0, command=self.pause_timer,
                                   state=DISABLED)
        self.pause_button.grid(column=1, row=4)

        self.reset_button = Button(text="Reset", bg=YELLOW, highlightthickness=0, borderwidth=0, command=self.reset_timer)
        self.reset_button.grid(column=2, row=4)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = PomodoroTimer()
    app.run()
