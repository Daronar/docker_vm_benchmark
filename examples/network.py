
name = "network"

install_cmd = "phoronix-test-suite install pts/network"

run_cmd = "printf 'y\nnet0\nnet0\nsimple_net\nn\nn' | phoronix-test-suite run pts/network"

execution_time = 120 #minutes

result_cmd = "cat .phoronix-test-suite/test-results/net0/test-1.xml | grep 'Value'"

clear_result = "rm -r .phoronix-test-suite/test-results/net0"

def result_function(result):
    f = result.split('>')
    f = f[1].split('<')
    return f[0]