def get_device_id() -> str:
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:6] == 'Serial':
                cpuserial = line[10:26]
        f.close()
    except BaseException:
        cpuserial = "ERROR000000000"
    return cpuserial
