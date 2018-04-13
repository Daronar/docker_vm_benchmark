
name = "john_the_ripper"

install_cmd = "phoronix-test-suite install pts/john-the-ripper"

run_cmd = "printf '3\ny\njtr\njtr\nsimple_jtr\nn\nn' | phoronix-test-suite run pts/john-the-ripper"

execution_time = 120 #minutes

result_cmd = "cat .phoronix-test-suite/test-results/jtr/test-1.xml | grep 'Value'"

clear_result = "rm -r .phoronix-test-suite/test-results/jtr"

def result_function(result):
    f = result.split('>')
    f = f[1].split('<')
    return f[0]