import sys
from test_organisation.test import Test
from test_organisation.test_exuctor import TestExecutor

# def main_function(type_of_carrier, path_to_test, cpu_for_instance, ram_for_instance, )

if __name__ == "__main__":
    type_of_carrier = sys.argv[1]
    path_to_test = sys.argv[2]
    cpu_for_instance = sys.argv[3]
    ram_for_instance = sys.argv[4]
    tries_amount = sys.argv[5]
    exp_desc = sys.argv[6]
    max_overlap = sys.argv[7]

    t = Test()
    t.load(path_to_test)


    te = TestExecutor()
    te.max_overlap_cpu = float(max_overlap)
    te.tries_num = int(tries_amount)
    if cpu_for_instance != "None":
        te.cpu_num = int(cpu_for_instance)
    if cpu_for_instance != "None":
        te.ram_num = int(ram_for_instance)

    te.set_test(t)
    te.set_factory(type_of_carrier)
    # main job
    te.create_path_for_result(exp_desc)


    try:
        te.execute_test_in_tries()
    except KeyboardInterrupt:
        te.close()
    except Exception:
        print("Are you ready to exit?:")
        ans = input()
        while ans != "Y":
            print("Are you ready to exit?:")
            ans = input()
        te.close()
    except BaseException:
        te.close()
    else:
        te.close()