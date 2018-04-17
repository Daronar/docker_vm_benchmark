
name = "stream"

install_cmd = "phoronix-test-suite install pts/stream"

run_cmd = "printf '4\ny\nramstream\nramstream\nsimple_stream\nn\nn' | phoronix-test-suite run pts/stream"

execution_time = 120 #minutes

result_cmd = "cat .phoronix-test-suite/test-results/ramstream/test-1.xml | grep 'Value'"

clear_result = "rm -r .phoronix-test-suite/test-results/ramstream-"

def result_function(result):
    f = result.split('>')
    f = f[1].split('<')
    return f[0]