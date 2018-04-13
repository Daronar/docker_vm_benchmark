
name = "ramspeed"

install_cmd = "phoronix-test-suite install pts/ramspeed"

run_cmd = "printf '4\n2\ny\nrs\nrs\nsimple_rs\nn\nn' | phoronix-test-suite run pts/ramspeed"

execution_time = 480 #seconds, maybe unused field

result_cmd = "cat .phoronix-test-suite/test-results/rs/test-1.xml | grep 'Value'"

clear_result = "rm -r .phoronix-test-suite/test-results/rs"

def result_function(result):
    f = result.split('>')
    f = f[1].split('<')
    return f[0]