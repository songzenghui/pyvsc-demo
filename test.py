import vsc
import json
import yaml

from collections import OrderedDict
f = open("/Users/songzenghui/Downloads/pyvsc-master/ve/unit/struct.json")
f_cfg = open("/Users/songzenghui/Downloads/pyvsc-master/ve/unit/config.yml")
data_cfg = yaml.load(f_cfg, Loader=yaml.FullLoader)
print(data_cfg)
data = json.load(f,object_pairs_hook=OrderedDict)
d=dict()
l = 0
one_s = "1"
zero_s = "0"
check_s = ""
for i, key in enumerate(data):
    x_s = ["x"]
    if i==0:
        l = max(data[key])
    # TODO
    x_s = x_s * l
    high_index = max(data[key]) 
    low_index = min(data[key]) 

    sli = slice(low_index, high_index+1)
    if key in data_cfg:
        check_values = data_cfg[key]["check_values"]
        for j, check_value in enumerate(check_values):
            if len(check_value) < (high_index - low_index + 1):
                check_value = check_value + "0" * (high_index - low_index + 1 - len(check_value))
            x_s[sli] = list(check_value)[0:high_index - low_index]
            check_s = "".join(["0b"]+ x_s)
            d[key+f"_check_value_{j}"] = vsc.wildcard_bin(check_s)
            print(f"{key}_check_value_{j} :{check_s}")
    else:
        x_s[sli] = ["1"] * (high_index - low_index + 1)
        one_s = "".join(["0b"]+ x_s)
        x_s[sli] = ["0"] * (high_index - low_index + 1)
        zero_s = "".join(["0b"] + x_s)
        print(f"{key}_one :{one_s}")
        print(f"{key}_zero:{zero_s}")

        d[key+"_one"] = vsc.wildcard_bin(one_s)
        d[key+"_zero"] = vsc.wildcard_bin(zero_s)
f.close()
f_cfg.close()
@vsc.covergroup
class cg(object):
    
    def __init__(self):
        self.with_sample(
            dict(a=vsc.bit_t(8)))
        
        self.cp_a = vsc.coverpoint(self.a, bins=d)
        
cg_i = cg()
# cg_i.sample(int("0x88", 16))
# cg_i.sample(int("0x8a", 16))
cg_i.sample(int("0b00000000000000000000", 2))
# self.assertEqual(cg_i.get_coverage(), 0.0)

# for i in range(16):        
#     cg_i.sample(0x80+i)
    # self.assertEqual(cg_i.get_coverage(), 100*((1+i)/16))
vsc.report_coverage(details=True)