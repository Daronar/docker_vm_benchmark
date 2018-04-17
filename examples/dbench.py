
name = "dbench"

install_cmd = "phoronix-test-suite install pts/dbench"

run_cmd = "printf '3\ny\ndbench0\ndbench0\nsimple_dbench\nn\nn' | phoronix-test-suite run pts/dbench"

execution_time = 120 #minutes

result_cmd = "cat .phoronix-test-suite/test-results/dbench0/test-1.xml | grep 'Value'"

clear_result = "rm -r .phoronix-test-suite/test-results/dbench0"

def result_function(result):
    f = result.split('>')
    f = f[1].split('<')
    return f[0]