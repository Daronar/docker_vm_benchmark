# import subprocess
#
# # author Pavel Mikheev
#
# test_num = 3
#
# carrier_types = ["docker", "kvm", "dockerinvm"]
#
# test_names = ["aio", "cachebench", "dbench", "gzip", "john-the-ripper", "nginx", "pybench", "ramspeed", "stream"]
#
# run_cmd = "python3 main.py %s examples.%s 4 512 3 %s 50.0"
#
# for car_type in carrier_types:
#     for test in test_names:
#         name = '_'.join([car_type, test, "great"])
#         cur_cmd = run_cmd%(car_type, test, name)
#         cmd = subprocess.Popen(cur_cmd.split(' '), stdout=subprocess.PIPE)
#         cmd.wait()
#
# run_cmd = "python3 main.py %s examples.%s None None 3 %s 200.0"
#
# for car_type in carrier_types:
#     for test in test_names:
#         name = '_'.join([car_type, test, "none"])
#         cur_cmd = run_cmd % (car_type, test, name)
#         cmd = subprocess.Popen(cur_cmd.split(' '), stdout=subprocess.PIPE)
#         cmd.wait()
#!/bin/sh

# python3 main.py docker examples.ramspeed 4 256 1 ramspeed_docker_great 8.0

# python3 main.py kvm examples.ramspeed 4 256 1 ramspeed_kvm_great 5.6

