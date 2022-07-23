# --------------------------------------------#
# summary.py
# 该部分代码只用于看网络结构，并非测试代码
# --------------------------------------------#
import defaults
from nets.pspnet import pspnet

if __name__ == "__main__":
    model = pspnet(input_shape=[473, 473, 3],
                   num_classes=defaults.num_classes,
                   down_sample_factor=defaults.down_sample_factor,
                   backbone=defaults.backbone,
                   aux_branch=False)
    model.summary()

    for i, layer in enumerate(model.layers):
        print(i, layer.name)
