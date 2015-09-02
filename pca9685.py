#coding=UTF-8

import smbus

pca9685_addr = 0x40
bus = smbus.SMBus(1)


def set_sleep(addr):
    reg_model = 0x00
    sleep_bit = 0x01 << 4
    old_model_val = bus.read_i2c_block_data(addr, reg_model, 1)
    bus.write_i2c_block_data(addr, reg_model, [old_model_val | sleep_bit])

def unset_sleep(addr):
    reg_model = 0x00
    sleep_bit = 0x01 << 4
    old_model_val = bus.read_i2c_block_data(addr, reg_model, 1)
    bus.write_i2c_block_data(addr, reg_model, [old_model_val & ~(sleep_bit)])


#LEDx_ON_L  = 0x06 + 4 * x
#LEDx_ON_H  = 0x07 + 4 * x
#LEDx_OFF_L = 0x08 + 4 * x
#LEDx_OFF_H = 0x09 + 4 * x
def set_PWM_ON(addr, ch, value):
    low_byte_val = value & 0x00FF
    high_byte_val = (value & 0x00FF) >> 8
    reg_low_byte = 0x06 + ch * 4
    bus.write_i2c_block_data(addr, reg_low_byte, [low_byte_val])
    bus.write_i2c_block_data(addr, reg_low_byte + 1, [high_byte_val])

def set_PWM_OFF(addr, ch, value):
    low_byte_val = value & 0x00FF
    high_byte_val = (value & 0x0FF) >> 8
    reg_low_byte = 0x08 + ch * 4
    bus.write_i2c_block_data(addr, reg_low_byte, [low_byte_val])
    bus.write_i2c_block_data(addr, reg_low_byte + 1, [high_byte_val])

def main():
    #set prescale PWM frequency = 50Hz
    bus.write_i2c_block_data(pca9685_addr, 0xFE, [121])

    #exit sleep mode
    bus.write_i2c_block_data(pca9685_addr, 0x00, [0x01])

    #set zero PWM channel output dutycycle = 1024 / 4096
    set_PWM_OFF(pca9685_addr, 0, 1024)

if __name__ == 'main':
    main()

