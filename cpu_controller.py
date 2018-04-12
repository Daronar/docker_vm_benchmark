import SETTINGS

class CPUController:
    def __init__(self):
        self.last_used_num = -1
        self.max_num = SETTINGS.CPU_NUM - 1

    def get_new_set(self, num):
        set = []
        first_pos = (self.last_used_num+1)%(self.max_num+1)
        if self.last_used_num + num > self.max_num:
            if first_pos != 0:
                for i in range(first_pos, self.max_num+1):
                    set.append(i)
            last = (self.last_used_num + num)%(self.max_num + 1)
            for i in range(0, last+1):
                set.append(i)
            self.last_used_num = last
        else:
            for i in range(first_pos, self.last_used_num + num + 1):
                set.append(i)
            self.last_used_num = self.last_used_num + num
        return ','.join(map(str, set))

c = CPUController()
num = 4
for i in range(10):
    print(c.get_new_set(num), end='||')
