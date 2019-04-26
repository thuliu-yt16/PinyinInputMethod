import codecs, re, os, json
import cPickle as pickle
from math import log
class PinyinInputMethod:
    def __init__(self,path):
        self.model = pickle.load(open(path + 'char_binary_model/binary_model', 'r'))
        self.global_info = pickle.load(open(path + 'char_binary_model/global_info', 'r'))
        self.pinyin_table = pickle.load(open(path + 'char_binary_model/pinyin2char','r'))

        if self.model and self.global_info:
            print 'Init Done'
        else:
            print 'Init Error'

    def find_mps(self,sentence,lam):
        model = self.model
        global_info = self.global_info
        pinyin_table = self.pinyin_table
        pinyin_list = sentence.lower().split(' ')
        while '' in pinyin_list:
            pinyin_list.remove('')

        def P_i(w):
            try:
                return log(model[w]['be_init']) - log(global_info['be_init'])
            except (KeyError, ValueError):
                return -1e4

        def P_w(w1, w2):
            try:
                return log((1 - lam) * model[w1]['suffix'][w2] * 1.0 / model[w1]['be_prefix'] + lam * model[w1][
                    'total'] * 1.0 / global_info['total'])
            except (KeyError, ValueError):
                return -1e4

        def P_p(w, p):
            try:
                return log(model[w]['pinyin'][p]) - log(model[w]['pinyin_total'])
            except (KeyError, ValueError):
                return -1e4
        '''
        def P_i(w):
            return log(model[w]['be_init']) - log(global_info['be_init']) if w in model and model[w]['be_init'] > 0 else -1e4
        
        def P_w(w1,w2):
            return log((1-lam)*model[w1]['suffix'][w2]*1.0/model[w1]['be_prefix'] + lam*model[w1]['total']*1.0/global_info['total']) if w1 in model and w2 in model[w1]['suffix'] else -1e4

        def P_p(w,p):
            return log(model[w]['pinyin'][p]) - log(model[w]['pinyin_total']) if w in model and p in model[w]['pinyin'] else -1e4
        
        '''

        sts = [(c,c,P_i(c) + P_p(c,pinyin_list[0])) for c in pinyin_table[pinyin_list[0]]]

        for pinyin in pinyin_list[1:]:
            sts = [max([(st[0] + c, c , st[2] + P_w(st[1],c) + P_p(c,pinyin)) for st in sts],key = lambda x : x[2]) for c in pinyin_table[pinyin]]

        return max(sts, key = lambda x : x[2])[0]

    def test(self,input_path,output_path):
        with open(input_path, 'r',)  as f:
            lines = f.readlines()

        output = [self.find_mps(line.strip(),0) for line in lines]
        with open(output_path,'w') as f:
            f.write('\n'.join(output).encode('utf-8'))
