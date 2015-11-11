def decodeLoc(value, mask):
    ########################################################
    # Decode the location from the AprilTag value
    ########################################################
    value = (~value + (value << 21)) & mask
    value = value ^ value >> 24
    value = ((value + (value << 3)) + (value << 8)) & mask
    value = value ^ value >> 14
    value = ((value + (value << 2)) + (value << 4)) & mask
    value = value ^ value >> 28
    value = (value + (value << 31)) & mask
    return value


for x in xrange(10):
    print decodeLoc(x, (1<<8)-1)