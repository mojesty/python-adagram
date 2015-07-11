import sys

import numpy as np

from softmax import build_huffman_tree, convert_huffman_tree


class Dictionary(object):
    def __init__(self, freqs, id2word):
        assert len(freqs) == len(id2word)
        self.freqs = freqs
        self.id2word = id2word
        self.word2id = {w: id_ for id_, w in enumerate(self.id2word)}

    @classmethod
    def read(cls, filename, min_freq):
        words_freqs = []
        with open(filename, 'rb') as f:
            for n, line in enumerate(f, 1):
                line = line.decode('utf-8').strip()
                try:
                    word, freq = line.split()
                    freq = int(freq)
                except ValueError:
                    print >>sys.stderr, \
                        u'Expected "word freq" pair on line {}, got "{}"'\
                        .format(n, line)
                    sys.exit(1)
                if freq >= min_freq:
                    words_freqs.append((word, freq))
        words_freqs.sort(key=lambda (w, f): f, reverse=True)
        return cls([f for _, f in words_freqs], [w for w, _ in words_freqs])

    def __len__(self):
        return len(self.id2word)


class VectorModel(object):
    '''
    code::DenseArray{Int8, 2}
    path::DenseArray{Int32, 2}
    In::DenseArray{Tsf, 3}
    Out::DenseArray{Tsf, 2}
    alpha::Float64
    counts::DenseArray{Float32, 2}
    '''
    def __init__(self, freqs, dim, prototypes, alpha):
	N = len(freqs)
	nodes = build_huffman_tree(freqs)
	outputs = convert_huffman_tree(nodes, N)

        max_length = max(len(x.code) for x in outputs)
	self.path = np.zeros((max_length, N), dtype=np.int32)
	self.code = np.zeros((max_length, N), dtype=np.int8)

       #for n in 1:N
       #	code[:, n] = -1
       #	for i in 1:length(outputs[n])
       #		code[i, n] = outputs[n].code[i]
       #		path[i, n] = outputs[n].path[i]
       #	end
       #end

        self.In = rand_arr((dim, prototypes, N), dim)
        self.Out = rand_arr((dim, N), dim)
	self.counts = np.zeros((prototypes, N), np.float32)
	self.frequencies = np.array(freqs, dtype=np.int64)
        self.alpha = alpha


def rand_arr(shape, inv_norm):
    return (np.random.rand(*shape) - 0.5) / inv_norm