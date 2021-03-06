import rospy

MIN_NUM = float('-inf')
MAX_NUM = float('inf')


class PID(object):
    def __init__(self, kp, ki, kd, mn=MIN_NUM, mx=MAX_NUM):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.min = mn
        self.max = mx

        self.int_val  = self.last_error = 0.
        self.int_list = [0,0,0,0,0,0,0,0,0]

    def reset(self):
        self.int_val = 0.0
        self.last_error = 0.
        self.int_list = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    def step(self, error, sample_time):

        # use a list of 10 errors
        self.int_list.pop(0)
        self.int_list.append(error*sample_time)

        derivative = (error - self.last_error) / sample_time;

        y = self.kp * error + self.ki * self.int_val + self.kd * derivative;
        # rospy.loginfo("P %.03f  I:%.03f, D:%.03f", self.kp * error, self.ki * self.int_val, self.kd * derivative)
        val = max(self.min, min(y, self.max))

        if val > self.max:
            val = self.max
        elif val < self.min:
            val = self.min
        else:
            self.int_val = sum(self.int_list)

        self.last_error = error

        return val
