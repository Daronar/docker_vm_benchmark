import matplotlib.pyplot as plt
import sys
import json


def read_from_file(path_to_file, overlap_from=None, overlap_till=None):
    f = open(path_to_file).read()
    txt = "[" + f.replace("}{", "},\n{") + "]"
    test_result = json.loads(txt)
    medians = []
    averages = []
    ovelaps = []
    for step in test_result:
        if overlap_from is not None and step["overlap"] < overlap_from:
            continue
        if overlap_till is not None and step["overlap"] > overlap_till:
            break
        medians.append(step["total_median"])
        averages.append(step["total_average"])
        ovelaps.append(step["overlap"])
    return medians, averages, ovelaps

def comparison(d_o, v_o, d_m, v_m, d_a, v_a, file_name, desc="simple"):
    m_dif = []
    a_dif = []
    if len(d_o) < len(v_o):
        v_o = v_o[0:len(d_o)]

    for i in range(len(v_o)):
        m_dif.append(d_m[i] - v_m[i])
        a_dif.append(d_a[i] - v_a[i])

    plt.figure(3)

    l1, l2 = plt.plot(v_o, m_dif, 'r^-', v_o, a_dif, 'g^-')

    plt.legend((l1, l2), (u'Median', u'Average'), loc="upper center")

    plt.xlabel('Overlap')

    plt.ylabel('Difference between Docker perfomance and KVM perfomance')

    plt.title(desc)

    plt.grid(True)

    plt.savefig(file_name + "_difference.png", dpi=300)

def real_graphic(d_o, v_o, d_m, v_m, d_a, v_a, file_name):
    plt.figure(1)

    line1, line2 = plt.plot(d_o, d_m, 'bD:', v_o, v_m, 'go:')

    plt.legend((line1, line2),
               (u'Results for containers', u'Results for VM'), loc="upper center")

    plt.xlabel('Overlap')

    plt.ylabel('Perfomance (median)')

    plt.grid(True)

    plt.savefig(file_name + "_median.png", dpi=300)

    plt.figure(2)

    line1, line2 = plt.plot(d_o, d_a, 'bD:', v_o, v_a, 'go:')

    plt.legend((line1, line2),
               (u'Results for containers', u'Results for VM'), loc="upper center")

    plt.xlabel('Overlap')

    plt.ylabel('Perfomance (average)')

    plt.grid(True)

    plt.savefig(file_name + "_average.png", dpi=300)



if __name__ == "__main__":
    path_to_docker = sys.argv[1]
    path_to_kvm = sys.argv[2]
    # path_to_dockerinvm = sys.argv[3]
    # desc = sys.argv[4]
    desc = sys.argv[3]
    file_name = sys.argv[4]

    if len(sys.argv) > 5:
        overlap_from = float(sys.argv[5])
        overlap_till = float(sys.argv[6])
    else:
        overlap_till = None
        overlap_from = None

    d_ms, d_as, d_os = read_from_file(path_to_docker, overlap_from, overlap_till)

    v_ms, v_as, v_os = read_from_file(path_to_kvm, overlap_from, overlap_till)

    real_graphic(d_os, v_os, d_ms, v_ms, d_as, v_as, file_name)

    comparison(d_os, v_os, d_ms, v_ms, d_as, v_as, file_name, desc)


    # line1, line2 = plt.plot(d_os, d_ms, 'bD:', v_os, v_ms, 'go:')
    #
    # plt.legend((line1, line2),
    #            (u'Results for containers', u'Results for VM'), loc="upper center")
    #
    # # i_ms, i_as, i_os = read_from_file(path_to_dockerinvm)
    #
    # # line1, line2, line3 = plt.plot(d_ms, d_os, 'bD:', v_ms, v_os, 'go:', i_ms, i_os, 'r^-')
    # #
    # # plt.legend((line1, line2, line3),
    # #            (u'Results for containers', u'Results for VM', u'Results for DockerInVM'), loc="upper center")
    #
    # plt.xlabel('Overlap')
    #
    # plt.ylabel('Perfomance')
    #
    # plt.title(desc)
    #
    # plt.grid(True)
    #
    # plt.show()


