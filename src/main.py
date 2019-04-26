import sys,time
from Pinyin.PinyinInputMethod import PinyinInputMethod

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: python main.py path_of_input_file path_of_output_file'
    else:
        begin_time = time.time()
        input_path ,output_path = sys.argv[1], sys.argv[2]
        pinyininput = PinyinInputMethod('../data/')
        mid_time = time.time()
        print 'Init time:' + str(mid_time - begin_time) + 's'
        pinyininput.test(input_path,output_path)
        end_time = time.time()
        print 'Convert Done'
        print 'Convert time:' + str(end_time - mid_time) + 's'

