TOTAL_DIVS = 100


def write_cmd(dest, num):
    with open(dest, 'w') as cmd_out:
        cmd_out.write("universe              = vanilla\n")
        cmd_out.write("executable            = eng_counts.sh\n")
        cmd_out.write("getenv                = true\n")
        cmd_out.write("error                 = error/eng_counts" + str(num) + ".err\n")
        cmd_out.write("log                   = log/eng_counts" + str(num) + ".log\n")
        cmd_out.write("output                = eng_counts" + str(num) + ".info\n")
        cmd_out.write("arguments             = \"" + str(num) +"\"\n")
        cmd_out.write("transfer_executable   = false\n")
        cmd_out.write("queue\n")


if __name__ == '__main__':
    for div_num in range(TOTAL_DIVS):
        output_name = "/home2/egarnick/courses/LOR/eng_counts" + str(div_num) + ".cmd"
        write_cmd(output_name, div_num)
        print("Wrote: " + output_name)
