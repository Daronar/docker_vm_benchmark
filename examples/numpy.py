
name = "numpy"

install_cmd = "apt install -y python;apt install -y python-pip;pip install numpy;phoronix-test-suite install pts/numpy"

run_cmd = "printf 'y\nnumpy0\nnumpy0\nsimple_numpy\nn\nn' | phoronix-test-suite run pts/numpy"

execution_time = 120 #minutes

result_cmd = "cat .phoronix-test-suite/test-results/numpy0/test-1.xml | grep 'Value'"

clear_result = "rm -r .phoronix-test-suite/test-results/numpy0"

def result_function(result):
    f = result.split('>')
    f = f[1].split('<')
    return f[0]