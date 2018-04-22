import SETTINGS
import time
from test_organisation.test import Test
from kvm.kvmfactory import KvmFactory
import os
from container.docker_factory import DockerFactory
import statistics
import json
from docker_in_vm.docker_in_vm_factory import DockerInVmFactory

class TestExecutor:
    def __init__(self):

        self.result_file = None

        self.carriers = []

        self.step = 1 # amount of new carriers

        self.cpu_num = None
        self.ram_num = None

        self.test = None

        self.carrier_type = None
        self.carrier_factory = None

        self.tries_num = 1

        self.current_overlap_cpu = 0.0
        self.max_overlap_cpu = 1.0

        self.test_result = {}

    def create_path_for_result(self, exc_desc):
        if not os.path.exists('results'):
            os.mkdir('results')
            os.chmod('results', 0o775)
        if not os.path.exists('results/' + exc_desc):
            os.mkdir('results/' + exc_desc)
            os.chmod('results/' + exc_desc, 0o775)
        self.result_file = 'results/' + exc_desc + '/' + str(self.test.name) + "_result.txt"
        f = open(self.result_file, 'w+')
        f.close()
        os.chmod(self.result_file, 0o666)

    def set_test(self, t: Test):
        self.test = t

    def set_factory(self, carrier_type):
        self.carrier_type = carrier_type
        if carrier_type == "kvm":
            self.carrier_factory = KvmFactory(self.cpu_num, self.ram_num)
            return "kvm"
        elif carrier_type == "docker":
            self.carrier_factory = DockerFactory(self.cpu_num, self.ram_num)
            return "docker"
        elif carrier_type == "dockerinvm":
            self.carrier_factory = DockerInVmFactory(self.cpu_num, self.ram_num)
        else:
            return None

    def update_condition(self):
        if self.cpu_num is None:
            self.current_overlap_cpu += self.step * 1.0
        else:
            self.current_overlap_cpu += self.step * (self.cpu_num / SETTINGS.CPU_NUM)

    def finish_condition(self):
        return self.current_overlap_cpu < self.max_overlap_cpu

    def start_test_in_carriers(self, alarm_time):
        full_cmd = "sleep $(( " + str(alarm_time) + " - $(date +%s) ));" + self.test.run_cmd
        # print("cmd to run = ", full_cmd)
        for i in range(len(self.carriers) - 1):
            self.carriers[i].send_cmd_without_answer(full_cmd)
        # for car in self.carriers:
        #     print(car.send_cmd(full_cmd))
            # car.send_cmd_without_answer(full_cmd)

    def start_test_in_last_carrier(self, alarm_time):
        full_cmd = "sleep $(( " + str(alarm_time) + " - $(date +%s) ));" + self.test.run_cmd
        self.carriers[-1].send_cmd(full_cmd)

    def clear_results_in_carriers(self):
        if self.test.clear_cmd != "":
            for car in self.carriers:
                try:
                    car.send_cmd(self.test.clear_cmd)
                except Exception:
                    continue


    def get_results_from_carriers(self):
        current_results = []
        for car in self.carriers:
            try:
                current_results.append(float(self.test.result_function(car.send_cmd(self.test.result_cmd))))
            except Exception:
                print("Can't take the result, pass it")
        if len(current_results) == 0:
            raise BaseException("No result, stop test")
        return current_results
        # average = 0.0
        # for car in self.carriers:
        #     average += float(self.test.result_function(car.send_cmd(self.test.result_cmd)))
        # average /= len(self.carriers)
        # return average


    def save_results(self, history):
        f = open(self.result_file, 'a')
        # print(str(self.current_overlap_cpu) + ' ' + str(result))
        # f.write(str(self.current_overlap_cpu) + ' ' + str(result) + '\n')
        to_write = {}
        to_write.update({
            "overlap": self.current_overlap_cpu,
            "amount": len(self.carriers),
            "history": history,
            "total_average": statistics.mean([x["average"] for x in history]),
            "total_median": statistics.median([x["median"] for x in history])
        })
        f.write(json.dumps(to_write, indent=4, sort_keys=True))
        f.close()

    def execute_test_in_tries(self):
        while self.finish_condition():
            print("# 1. Start new carrier")
            for i in range(self.step):
                self.carriers.append(self.carrier_factory.start_test_carrier(self.test.name, self.test.install_cmd))
            print("# 1.5 Update condition")
            self.update_condition()
            # result_for_tries = []
            history = []
            for i in range(self.tries_num):
                print("Try number is", i)
                print("# 2. Compute test_organisation start time.")
                start_time = int(time.time()) + 10
                print("# 3. Start cmd in all carriers")
                self.start_test_in_carriers(start_time)
                print("# 4. Wait time of test (this time can increase while carriers' amount increase)")
                self.start_test_in_last_carrier(start_time)
                time.sleep(10)
                # time.sleep(10 + self.test.execution_time)
                print("# 5. Get results of test.")
                # self.test_result[len(self.carriers)] = self.get_results_from_carriers()
                # result_for_tries.append(self.get_results_from_carriers())
                try_results = self.get_results_from_carriers()
                history.append({
                    "try_number": i,
                    "carriers": try_results,
                    "median": statistics.median(try_results),
                    "average": statistics.mean(try_results)
                })
                print("# 6. Clear results of test")
                self.clear_results_in_carriers()
            self.save_results(history)

    def close(self):
        print("Destroying topology!")
        self.carrier_factory.destroy()
        print("Finish")

