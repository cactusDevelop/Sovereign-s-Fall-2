import time


class DeltaTimer:
    def __init__(self, target_fps=20):
        self.target_fps = target_fps
        self.frame_duration = 1.0 / target_fps
        self.last_frame_time = time.perf_counter()
        self.accumulated_time = 0.0

    def reset(self):
        self.last_frame_time = time.perf_counter()
        self.accumulated_time = 0.0

    def should_update_frame(self):
        current_time = time.perf_counter()
        delta_time = current_time - self.last_frame_time
        self.accumulated_time += delta_time
        self.last_frame_time = current_time

        if self.accumulated_time >= self.frame_duration:
            self.accumulated_time -= self.frame_duration
            return True
        return False

    def wait_for_next_frame(self):
        current_time = time.perf_counter()
        elapsed = current_time - self.last_frame_time
        wait_time = max(0, self.frame_duration - elapsed)

        if wait_time > 0:
            time.sleep(wait_time)

        self.last_frame_time = time.perf_counter()


_global_timer = DeltaTimer(target_fps=20)


def get_timer():
    return _global_timer