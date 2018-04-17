
name = "cachebench"

install_cmd = "phoronix-test-suite install pts/cachebench"

run_cmd = "printf '3\ny\ncacheb\ncacheb\ncacheb\nn\nn' | phoronix-test-suite run pts/cachebench"

execution_time = 120 #minutes

result_cmd = "cat .phoronix-test-suite/test-results/cacheb/test-1.xml | grep 'Value'"

clear_result = "rm -r .phoronix-test-suite/test-results/cacheb"

def result_function(result):
    f = result.split('>')
    f = f[1].split('<')
    return f[0]