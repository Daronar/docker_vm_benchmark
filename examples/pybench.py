
name = "pybench"

install_cmd = "apt install python3;phoronix-test-suite install pts/pybench"

run_cmd = "printf 'y\npyb0\npyb0\nsimple_pyb\nn\nn' | phoronix-test-suite run pts/pybench"

execution_time = 120 #minutes

result_cmd = "cat .phoronix-test-suite/test-results/pb0/test-1.xml | grep 'Value'"

clear_result = "rm -r .phoronix-test-suite/test-results/pb0"

def result_function(result):
    f = result.split('>')
    f = f[1].split('<')
    return f[0]