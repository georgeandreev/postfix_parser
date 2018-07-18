local function check_mx(task)
        local rspamd_util = require "rspamd_util"
        local logger=require "rspamd_logger"
        local lua_maps = require "lua_maps"
        -- finf ip in our list
        logger.infox(task, 'imhere %1', whitelisted_ip:get_key('188.73.151.21'))
        -- fvv
        local ip_addr = task:get_ip()
        if task:get_user() or (ip_addr and ip_addr:is_local()) then
                return 0
        end
        local recipients = task:get_recipients('smtp')
        local mx_domain
        for _,recipient in pairs(recipients) do
                local is_cheater = 1
                if recipient.domain then
                        mx_domain = recipient['domain']
                else
                        mx_domain = task:get_helo()
                end
                if mx_domain then
                         mx_domain = rspamd_util.get_tld(mx_domain)
                end
                -- HERE NEED TO MAKE GETTING IP FROM MX
                if is_cheater ~= 0 then
                        return 0
                end
        end
        return 1

end


-- Reading configuration

-- Get all options for this plugin
local opts =  rspamd_config:get_all_opt('check_our_mx')
local logger=require "rspamd_logger"
if opts then
    if opts['whitelisted_ip'] then
        config_param = opts['whitelisted_ip']
        whitelisted_ip = rspamd_map_add('check_our_mx', 'whitelisted_ip', 'radix', 'Greylist whitelist ip map')
        -- Register callback
        rspamd_config:register_symbol({
             callback = check_mx,
             type = 'prefilter',
             score = -6
        })
    end
end
