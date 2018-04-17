
name = "nginx"

install_cmd = "phoronix-test-suite install pts/nginx"

run_cmd = "printf 'y\nnginx0\nnginx0\nsimple_nginx\nn' | phoronix-test-suite run pts/nginx"

execution_time = 120 #minutes

result_cmd = "cat .phoronix-test-suite/test-results/nginx0/test-1.xml | grep 'Value'"

clear_result = "rm -r .phoronix-test-suite/test-results/nginx0"

def result_function(result):
    f = result.split('>')
    f = f[1].split('<')
    return f[0]