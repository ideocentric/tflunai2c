from TfLunaI2C import TfLunaI2C
import time
if __name__ == '__main__':
    tf = TfLunaI2C()
    print(tf)
    for i in range(10):
        data = tf.read_data()
        tf.print_data()
        time.sleep(0.5)
    '''
    tf.write_address(0x10)
    tf.save()
    tf.reboot()
    time.sleep(2)
    print(tf)
    '''