
name = "pgbench"

install_cmd = "phoronix-test-suite install pts/pgbench"

run_cmd = "printf '3\n3\n1\ny\npg1\npg1\npg1\nn\nn' | phoronix-test-suite run pts/pgbench"

execution_time = 120 #minutes

result_cmd = "cat .phoronix-test-suite/test-results/pg1/test-1.xml | grep 'Value'"

clear_result = "rm -r .phoronix-test-suite/test-results/pg1"

def result_function(result):
    f = result.split('>')
    f = f[1].split('<')
    return f[0]