require 'math'

local function ip2num(ip)
    local o1,o2,o3,o4 = ip:match("(%d+)%.(%d+)%.(%d+)%.(%d+)")
    local num = 2^24*o1 + 2^16*o2 + 2^8*o3 + o4
    return num
end

local str = '217.107.217.0/27'
local function split(s, delimiter)
    result = {};
    for match in (s..delimiter):gmatch("(.-)"..delimiter) do
        table.insert(result, match);
    end
    return result;
end

local function is_ip_in_network(ip, cidr)
    ip_num = ip2num(ip)
    local s = split(cidr, '/')

    local lower_ip = ip2num(s[1])
    local upper_ip = lower_ip + math.pow(2, 32-s[2]) - 1
    return ip_num > lower_ip and ip_num < upper_ip
end
