
name = "aio-stress"

install_cmd = "phoronix-test-suite install pts/aio-stress"

run_cmd = "printf 'y\naio\naio\nsimple_aio\nn\nn' | phoronix-test-suite run pts/aio-stress"

execution_time = 120 #minutes

result_cmd = "cat .phoronix-test-suite/test-results/aio/test-1.xml | grep 'Value'"

clear_result = "rm -r .phoronix-test-suite/test-results/aio"

def result_function(result):
    f = result.split('>')
    f = f[1].split('<')
    return f[0]