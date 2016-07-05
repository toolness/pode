def parse_secure_proxy_ssl_header(field):
    name, value = field.split(':')

    return ('HTTP_%s' % name.upper().replace('-', '_'), value.strip())
