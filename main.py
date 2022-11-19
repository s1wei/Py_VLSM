# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import IPy


def exchange_maskint(mask_int):
    bin_arr = ['0' for i in range(32)]
    for i in range(mask_int):
        bin_arr[i] = '1'
    tmpmask = [''.join(bin_arr[i * 8:i * 8 + 8]) for i in range(4)]
    tmpmask = [str(int(tmpstr, 2)) for tmpstr in tmpmask]
    return '.'.join(tmpmask)


def check_ip(address, net_mask):
    # 判断ip是否正确
    try:
        IPy.IP(address).make_net(net_mask)
    except:
        return False
    else:
        print(IPy.IP(address).make_net(net_mask))
        return True


def count_host(ip_address, mask, SubNetNum):
    net_arr = []
    for i in range(1, int(SubNetNum) + 1):
        net_num = input("请输入第" + str(i) + "个子网的主机数量:")

        for j in range(1, 32):
            if (2 ** j) >= int(net_num) + 2:
                net_dict = {
                    "net_num": int(net_num),
                    "net_space": (2 ** j) - 2,
                    "host_bit": j
                }
                net_arr.append(net_dict)
                break

    sum_space = 0
    for k in range(0, len(net_arr)):

        sum_space = sum_space + (int(net_arr[k]["net_space"])+2)     # 可用主机总和，用于判断主机数是否可以满足

    HostMax = int(2 ** int(32 - int(mask)))
    if sum_space > HostMax:
        print("划分主机数不够分配，可以尝试增大主机位解决")
    else:
        print("划分合法，进行一键划分操作")
        VLSM(ip_address, net_arr)


def VLSM(ip_address,net_arr):

    vlsm_arr = []

    int_address = ip_address.int()

    for i in range(0, len(net_arr)):
        arr_num = net_arr[i]["net_num"]
        arr_space = net_arr[i]["net_space"]
        arr_bit = net_arr[i]["host_bit"]
        # print("第" + str(i + 1) + "个：需要主机数量:" + str(arr_num) + ",分配主机数量:" + str(arr_space) + ",主机位:" + str(arr_bit))

        network_address = str(IPy.IP(int_address))
        subnet_mask = str(exchange_maskint((32-arr_bit)))
        prefix = str(32-arr_bit)
        first_host_address = str(IPy.IP(int_address+1))
        end_host_address = str(IPy.IP(int_address + arr_space))
        broadcast_address = str(IPy.IP(int_address + arr_space + 1))
        host_num = str(arr_space)

        int_address = int_address + arr_space + 2   # 这里的ip被用了，加上

        subnetting = {
            "network_address": network_address,
            "subnet_mask": subnet_mask,
            "prefix": prefix,
            "first_host_address": first_host_address,
            "end_host_address": end_host_address,
            "broadcast_address": broadcast_address,
            "host_num": host_num
        }

        # print(subnetting)

        vlsm_arr.append(subnetting)
    print("网络地址         子网掩码            前缀   第一个主机地址     最后一个主机地址     广播地址    可用主机数")
    for j in range(0, len(vlsm_arr)):
        vlsm_N_A = vlsm_arr[j]["network_address"]
        vlsm_S_M = vlsm_arr[j]["subnet_mask"]
        vlsm_P = vlsm_arr[j]["prefix"]
        vlsm_F_H_A = vlsm_arr[j]["first_host_address"]
        vlsm_E_H_A = vlsm_arr[j]["end_host_address"]
        vlsm_B_A = vlsm_arr[j]["broadcast_address"]
        vlsm_H_N = vlsm_arr[j]["host_num"]
        print("%-15s %-18s %-5s %-15s %-15s %-15s %-5s" % (vlsm_N_A, vlsm_S_M, vlsm_P, vlsm_F_H_A, vlsm_E_H_A, vlsm_B_A, vlsm_H_N))


if __name__ == '__main__':

    ip_address = input("请输入划分的网络地址：")
    mask = input("请输入子网前缀：")
    if check_ip(ip_address, mask):

        ip_address = IPy.IP(ip_address).make_net(mask)
        SubNet_num = input("请输入划分子网数量：")
        count_host(ip_address, mask, SubNet_num)

    else:
        print("请输入合法的ip地址和前缀!!!")
