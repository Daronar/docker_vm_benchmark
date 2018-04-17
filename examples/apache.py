name = "apache"

install_cmd = "apt-get -y install libexpat1-dev;printf '3\n' | phoronix-test-suite install pts/apache-1.7.1"

run_cmd = "printf 'y\napache0\napache0\napache0\nn\nn' | phoronix-test-suite run pts/apache-1.7.1"

execution_time = 120 #minutes

result_cmd = "cat .phoronix-test-suite/test-results/apache0/test-1.xml | grep 'Value'"

clear_result = "rm -r .phoronix-test-suite/test-results/apache0"

def result_function(result):
    f = result.split('>')
    f = f[1].split('<')
    return f[0]