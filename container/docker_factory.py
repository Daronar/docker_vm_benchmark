from container.dockercontainer import DockerContainer
from helpers.cpu_controller import CPUController
import docker
import SETTINGS
import time

class DockerFactory:
    def __init__(self, cpu_num=None, ram_num=None):
        self.base_image = ""
        self.conn = docker.from_env()
        self.cpu_con = CPUController()
        self.cpu_num = cpu_num
        self.ram_num = ram_num
        self.workers = []

    def destroy(self):
        for con in self.workers:
            self.destroy_container(con)
        self.conn.images.remove(image=self.base_image)

    def destroy_container(self, dc):
        dc.container.stop()
        dc.container.remove()

    def start_container(self, dc):
        run_args = {}
        dc.cpu_set = None
        if self.cpu_num is not None:
            cpu_set = self.cpu_con.get_new_set(self.cpu_num)
            run_args.update({"cpuset_cpus": cpu_set})
            dc.cpu_set = cpu_set
        if self.ram_num is not None:
            memory = self.ram_num
            run_args.update({"mem_limit": str(memory)+'m'})
        return self.conn.containers.run(image=dc.image, tty=True, detach=True, name=dc.name,
                                        working_dir="/root", command="bash", **run_args)

    def start_test_carrier(self, test_name, install_cmd):
        dc = DockerContainer()
        if len(self.workers) == 0:
            base_name = test_name + '_base'
            print("# 1. Start base container")
            base = self.conn.containers.run(image=SETTINGS.BASE_IMAGE, tty=True, detach=True, name=base_name, command="bash")
            print("# 2. Install test in base container")
            base.exec_run(cmd=install_cmd)
            print("# 3. Commit base container as image for tests")
            base.commit(test_name)
            self.base_image = test_name
            print("# 4. Stop base container")
            base.stop()
            print("# 5. Remove base container")
            base.remove()
        print("# 6. Run test carrier")
        carrier_name = test_name + str(len(self.workers))
        dc.name = carrier_name
        dc.image = self.base_image
        dc.container = self.start_container(dc)
        self.workers.append(dc)
        return dc


if __name__ == "__main__":
    df = DockerFactory(2, 1024)
    dc = df.start_test_carrier("chlech", "phoronix-test-suite install pts/ramspeed")
    cur_time = int(time.time())
    alarm_time = cur_time + 60
    dc.send_cmd("sleep $(( " + str(alarm_time) + " - $(date +%s) ))")
    print(int(time.time() - cur_time))
    df.destroy()
