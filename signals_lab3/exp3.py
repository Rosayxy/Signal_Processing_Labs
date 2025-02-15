import numpy as np
import matplotlib.pyplot as plt

# 时长为1秒
t = 1
# 采样率为60hz
fs = 60
t_split = np.arange(0, t * fs)


# 1hz与25hz叠加的正弦信号
x_1hz = t_split * 1 * np.pi * 2 / fs
x_25hz = t_split * 25 * np.pi * 2 / fs
signal_sin_1hz = np.sin(x_1hz)
signal_sin_25hz = np.sin(x_25hz)

signal_sin = signal_sin_1hz + 0.25 * signal_sin_25hz


# TODO: 补全这部分代码
# 通带边缘频率为10Hz，
# 阻带边缘频率为22Hz，
# 阻带衰减为44dB，窗内项数为17的汉宁窗函数
# 构建低通滤波器
# 函数需要返回滤波后的信号
# need to implement convolve function manually
def manual_convolve_same(x, h):

    Nx = len(x)
    Nh = len(h)
    out_len = Nx + Nh - 1

    full_conv = [0.0] * out_len
    for n in range(out_len):
        s = 0.0
        for k in range(Nh):
            x_idx = n - k
            if 0 <= x_idx < Nx:
                s += x[x_idx] * h[k]
                
        full_conv[n] = s
        
    # return the same length as x
    return full_conv[0 : 0 + Nx]

def filter_fir(input_signal):
    # M 直接给出了
    M = 17

    fc = 16 / fs
    n = np.arange(M)
    alpha = (M-1)/2
    window = 0.5 + 0.5 * np.cos(2 * np.pi * (n-alpha) / (M - 1))

    alpha = (M - 1) / 2

    h_ideal = 2 * fc * np.sinc(2 * fc * (n - alpha))

    h = h_ideal * window
    y = manual_convolve_same(input_signal, h)
    return y


# TODO: 首先正向对信号滤波(此时输出信号有一定相移)
# 将输出信号反向，再次用该滤波器进行滤波
# 再将输出信号反向
# 函数需要返回零相位滤波后的信号
def filter_zero_phase(input_signal):
    # 第一次正向滤波
    y_forward = filter_fir(input_signal)
    # 反转
    y_forward_rev = y_forward[::-1]
    # 第二次滤波
    y_rev_filtered = filter_fir(y_forward_rev)
    # 再次反转
    y_zero_phase = y_rev_filtered[::-1]
    return y_zero_phase

if __name__ == "__main__":
    delay_filtered_signal = filter_fir(signal_sin)
    zerophase_filtered_signal = filter_zero_phase(signal_sin)

    plt.plot(t_split, signal_sin, label = 'origin')
    plt.plot(t_split, delay_filtered_signal, label = 'fir')
    plt.plot(t_split, zerophase_filtered_signal, label = 'zero phase')

    plt.show()
