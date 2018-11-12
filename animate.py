class Animator:
    #  TODO add common easing functions bezier values

    def __init__(self, initial, final, duration, **options):
        self.count = 0
        self.initial = float(initial)
        self.final = float(final)
        self.duration = float(duration)
        self.range = self.final - self.initial
        self.bezier = options.get("easing", CubicBezier(.08, .7, 0, 0.99))
        self.current_loop = None

    def get(self):
        if self.count == 100:
            self.count = 0
            return None
        self.count += 1
        return self.range * self.bezier.get((self.count * self.bezier.get_for_x(self.duration) / 100)) + self.initial

    def animate(self, element, attr):
        value = self.get()
        if value is None:
            element[attr] = self.final
            return
        element[attr] = value
        element.after(int(self.duration * 10), self.animate, element, attr)

    def update(self, initial, final, duration):
        self.initial = float(initial)
        self.final = float(final)
        self.duration = float(duration)
        self.range = self.final - self.initial


class CubicBezier:
    #  FIXME Bezier does not function with very small duration values
    """
    Inspired by Mozilla's KSpline bezier curve engine
    Utilises Newton Raphson iteration method to perform approximations for parametric cubic bezier function
    """
    NEWTON_ITERATIONS = 4
    NEWTON_MIN_SLOPE = 0.001
    SUBDIVISION_PRECISION = 0.0000001
    SUBDIVISION_MAX_ITERATIONS = 10

    def __init__(self, p0, p1, p2, p3):
        self.p1x = p0
        self.p1y = p1
        self.p2x = p2
        self.p2y = p3
        self.k_spline_table_size = 11
        self.step_size = 1 / (self.k_spline_table_size - 1)
        self.sample_values = [self.calc_bezier(i * self.step_size, p0, p2) for i in range(self.k_spline_table_size)]
        if self.p1x == self.p1y and self.p2x == self.p2y:
            self.get = self.linear_easing
        else:
            self.get = self.bezier_easing

    @staticmethod
    def linear_easing(t):
        return t

    def get_for_x(self, t):
        start, current_sample, last_sample = 0, 1, self.k_spline_table_size - 1
        while current_sample != last_sample and self.sample_values[current_sample] <= t:
            start += self.step_size
            current_sample += 1
        current_sample -= 1

        dist = (t - self.sample_values[current_sample]) / (
                self.sample_values[current_sample + 1] - self.sample_values[current_sample])
        guess_for_t = start + dist * self.step_size
        init_slope = self.get_slope(guess_for_t, self.p1x, self.p2x)
        if init_slope >= CubicBezier.NEWTON_MIN_SLOPE:
            return self.newton_raphson_iterate(t, guess_for_t)
        elif init_slope == 0:
            return guess_for_t
        else:
            return self.binary_subdivide(t, start, start + self.step_size)

    def bezier_easing(self, t):
        if t == 0:
            return 0
        if t == 1:
            return 1
        else:
            return self.calc_bezier(self.get_for_x(t), self.p1y, self.p2y)

    def calc_bezier(self, at, a1, a2):
        # checked
        return ((self.a(a1, a2) * at + self.b(a1, a2)) * at + self.c(a1)) * at

    def binary_subdivide(self, ax, a, b):
        # checked
        current_t = a + (b - a) / 2
        current_x = self.calc_bezier(current_t, self.p1x, self.p2x) - ax
        i = 1
        while abs(current_x) > CubicBezier.SUBDIVISION_PRECISION and i < CubicBezier.SUBDIVISION_MAX_ITERATIONS:
            if current_x > 0:
                b = current_t
            else:
                a = current_t
            current_t = a + (b - a) / 2
            current_x = self.calc_bezier(current_t, self.p1x, self.p2x) - ax
            i += 1
        return current_t

    def newton_raphson_iterate(self, ax, at_guess):
        # Newton Raphson iteration
        # checked
        for i in range(CubicBezier.NEWTON_ITERATIONS):
            current_slope = self.get_slope(at_guess, self.p1x, self.p2x)
            if current_slope == 0:
                return at_guess
            current_x = self.calc_bezier(at_guess, self.p1x, self.p2x) - ax
            at_guess -= current_x / current_slope
        return at_guess

    def get_slope(self, at, a1, a2):
        # checked
        return 3 * self.a(a1, a2) * at ** 2 + 2 * self.b(a1, a2) * at + self.c(a1)

    @staticmethod
    def a(a1, a2):
        return 1 - 3 * a2 + 3 * a1

    @staticmethod
    def b(a1, a2):
        return 3 * a2 - 6 * a1

    @staticmethod
    def c(a1):
        return 3 * a1


class FancyLoader:

    def __init__(self, label):
        self.label = label
        self.start = 9650
        self.stop = 9671
        self.current = self.start - 1
        self.load_allowed = False

    def load(self):
        if self.load_allowed:
            self.label.after(100, self.load)
        else:
            return
        self.current += 1
        self.label.config(text=chr(self.current))
        if self.current == self.stop:
            self.current = self.start

    def start_load(self):
        self.load_allowed = True
        self.load()

    def stop_load(self):
        self.load_allowed = False
