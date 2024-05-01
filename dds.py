import numpy as np


class Dds():

    def __init__(self, fd, freq, signal_width, init_phase=0, dc=True):
        
        self.dc = dc
        self.gen_table(signal_width)
        self.set_freq(fd, freq, init_phase)
        

    def gen_table(self, signal_width):

        self.signal_width = int(signal_width)
        self.amplitude = 2**(signal_width-1) - 1
        self.mem_size = int(2**signal_width/4)
        phase = np.linspace(0.0, np.pi/2, self.mem_size+1)
        self.mem_samples = np.array(self.amplitude * np.sin(phase))
        self.mem_samples = np.floor(self.mem_samples)

        self.first_quarter = 0
        self.second_quarter = np.floor(2**signal_width / 4)
        self.third_quarter = np.floor(2**signal_width / 2)
        self.fourth_quarter = np.floor(3 * 2**signal_width / 4)


    def set_freq(self, fd, freq, init_phase=0):

        if 2*freq > fd:
            raise Exception("Must 2*freq < fd")

        self.acc = int(np.ceil(init_phase * 2**self.signal_width / (2 * np.pi)))
        self.step = int(np.ceil(2**self.signal_width * freq / fd))


    def get(self):
        
        addr = self.acc

        if addr >= self.first_quarter and addr < self.second_quarter:
            sample = self.mem_samples[addr]

        elif addr >= self.second_quarter and addr < self.third_quarter:
            addr = int(2**self.signal_width / 2 - addr)
            sample = self.mem_samples[addr]

        elif addr >= self.third_quarter and addr < self.fourth_quarter:
            addr = int(addr - (2**self.signal_width / 2))
            sample = -self.mem_samples[addr]
        
        elif addr >= self.fourth_quarter:
            addr = int(2**self.signal_width - addr)
            sample = -self.mem_samples[addr]

        self.acc += self.step

        if self.acc >= (2**self.signal_width - 1):
            self.acc -= (2**self.signal_width - 1)

        if self.dc:
            sample = sample + 2**(self.signal_width-1)

        return sample
