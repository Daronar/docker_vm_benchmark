
name = "gzip"

install_cmd = "phoronix-test-suite install pts/compress-gzip-1.2.0"

run_cmd = "printf 'y\ngzip\ngzip\nsimple_gzip\nn\nn' | phoronix-test-suite run pts/compress-gzip-1.2.0"

execution_time = 120 #minutes

result_cmd = "cat .phoronix-test-suite/test-results/gzip/test-1.xml | grep 'Value'"

clear_result = "rm -r .phoronix-test-suite/test-results/gzip"

def result_function(result):
    f = result.split('>')
    f = f[1].split('<')
    return f[0]