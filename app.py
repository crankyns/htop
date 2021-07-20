import psutil as ps


def get_cpu():
    res = {}
    cpu_time = ps.cpu_times(percpu=True)
    res["time"] = {}
    for index, core in enumerate(cpu_time):
        res["time"][f"core_{index}"] = (core.user, core.system)
    res["load"] = ps.cpu_percent(percpu=True, interval=0.3)
    return res


def get_memory():
    memory = ps.virtual_memory()
    mem = [memory.total/1e+9, memory.available/1e+9,memory.used/1e+9, memory.percent]
    return mem


def get_disk():
    res = {}
    disk_partitions = ps.disk_partitions(all=False)
    res["partitions"] = {}
    for index, part in enumerate(disk_partitions, 1):
        res["partitions"][f"diskpart_{index}"]= (part.device, part.mountpoint,part.fstype)
    res["usage"] = ps.disk_usage('/')
    res["usage"] = res["usage"][0]/1e+9,res["usage"][1]/1e+9,res["usage"][2]/1e+9,res["usage"][3]
    return res

def get_process():
    proc = [(f"Process ID: {p.pid}", p.info) for p in ps.process_iter(['name','status','cpu_percent']) if p.info['status'] == ps.STATUS_RUNNING]
    return proc


def show(**kwargs):
    cpu_time_template = "User time for {0} {1:>10},\tsystem time for {0} {2:>10}\n"
    cpu_time_str = ""
    cpu = kwargs["cpu"]
    for key, value in cpu["time"].items():
        cpu_time_str += cpu_time_template.format(key, *value)
    print(cpu_time_str)

    cpu_load_template = "Load on the core_{0} is {1}%\n"
    cpu_load_str = ""
    for i, k in enumerate(cpu["load"]):
        cpu_load_str += cpu_load_template.format(i,k)
    print(cpu_load_str)
    
    mem = kwargs["mem"]
    mem_template = "System memory usage:\ntotal: {0:.2f} GB\navailable: {1:.2f} GB\nused: {2:.2f} GB\npercent: {3}%\n"
    mem_str = mem_template.format(*mem)
    print(mem_str)

    disk = kwargs["disk"]
    disk_partitions_template = "{0}:\tdevice {1}\tmountpoint '{2}' (fstype:{3})\n"
    disk_partitions_str = ""
    for key, value in disk["partitions"].items():
        disk_partitions_str += disk_partitions_template.format(key, *value)
    disk_usage_template = "Disk usage:\ntotal: {0:.2f} GB\nused: {1:.2f} GB\nfree: {2:.2f} GB\npercent: {3}%\n"
    disk_usage_str = disk_usage_template.format(*disk["usage"])
    print(disk_partitions_str)
    print(disk_usage_str)

    proc = kwargs["proc"]
    print(*proc, sep="\n")

    


def main():
    cpu_data = get_cpu()
    disk_data = get_disk()
    mem_data = get_memory()
    proc_data = get_process()

    show(
        cpu=cpu_data,
        disk=disk_data,
        mem=mem_data,
        proc=proc_data
    )

if __name__ == "__main__":
    main()
