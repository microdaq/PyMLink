class MLinkError(Exception):
    pass

class MLink:
    def __init__(self, ip):
        if ip == "999.999.999.999":
            raise MLinkError 
        _ = ip

    @staticmethod
    def ai_read(channels, *args):
        return [1.0]*len(channels)

    @staticmethod
    def disconnect():
        return True

    @staticmethod
    def get_str_hw_info():
        return 'MicroDAQ E2000-ADC09-DAC06-12'