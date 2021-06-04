from pprint import pprint

import tensorflow as tf
import numpy as np
import time
import datetime
import os
import network
from sklearn import metrics

FLAGS = tf.app.flags.FLAGS

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"

# embedding the position
def pos_embed(x):
    if x < -60:
        return 0
    if -60 <= x <= 60:
        return x + 61
    if x > 60:
        return 122


def main_for_evaluation():
# def main(_):
    pathname = "./model_custom/ATT_GRU_model-"

    wordembedding = np.load('chinese_RE/custom_RE/vec.npy')

    test_settings = network.Settings()
    test_settings.vocab_size = 16693
    test_settings.num_classes = 16
    test_settings.big_num = 5561

    big_num_test = test_settings.big_num

    with tf.Graph().as_default():

        sess = tf.Session()
        with sess.as_default():

            def test_step(word_batch, pos1_batch, pos2_batch, y_batch):

                feed_dict = {}
                total_shape = []
                total_num = 0
                total_word = []
                total_pos1 = []
                total_pos2 = []

                for i in range(len(word_batch)):
                    total_shape.append(total_num)
                    total_num += len(word_batch[i])
                    for word in word_batch[i]:
                        total_word.append(word)
                    for pos1 in pos1_batch[i]:
                        total_pos1.append(pos1)
                    for pos2 in pos2_batch[i]:
                        total_pos2.append(pos2)

                total_shape.append(total_num)
                total_shape = np.array(total_shape)
                total_word = np.array(total_word)
                total_pos1 = np.array(total_pos1)
                total_pos2 = np.array(total_pos2)

                feed_dict[mtest.total_shape] = total_shape
                feed_dict[mtest.input_word] = total_word
                feed_dict[mtest.input_pos1] = total_pos1
                feed_dict[mtest.input_pos2] = total_pos2
                feed_dict[mtest.input_y] = y_batch

                loss, accuracy, prob = sess.run(
                    [mtest.loss, mtest.accuracy, mtest.prob], feed_dict)
                return prob, accuracy

           
            with tf.variable_scope("model"):
                mtest = network.GRU(is_training=False, word_embeddings=wordembedding, settings=test_settings)

            names_to_vars = {v.op.name: v for v in tf.global_variables()}
            saver = tf.train.Saver(names_to_vars)

        
            #testlist = range(1000, 1800, 100)
            testlist = [8100, 8200, 8300, 8400, 8500, 8600, 8700, 8800]
            
            for model_iter in testlist:
                # for compatibility purposes only, name key changes from tf 0.x to 1.x, compat_layer
                saver.restore(sess, pathname + str(model_iter))


                time_str = datetime.datetime.now().isoformat()
                print(time_str)
                print('Evaluating all test data and save data for PR curve')

                test_y = np.load('chinese_RE/custom_RE/testall_y.npy', allow_pickle=True)
                test_word = np.load('chinese_RE/custom_RE/testall_word.npy', allow_pickle=True)
                test_pos1 = np.load('chinese_RE/custom_RE/testall_pos1.npy', allow_pickle=True)
                test_pos2 = np.load('chinese_RE/custom_RE/testall_pos2.npy', allow_pickle=True)
                allprob = []
                acc = []
                for i in range(int(len(test_word) / float(test_settings.big_num))):
                    prob, accuracy = test_step(test_word[i * test_settings.big_num:(i + 1) * test_settings.big_num],
                                               test_pos1[i * test_settings.big_num:(i + 1) * test_settings.big_num],
                                               test_pos2[i * test_settings.big_num:(i + 1) * test_settings.big_num],
                                               test_y[i * test_settings.big_num:(i + 1) * test_settings.big_num])
                    acc.append(np.mean(np.reshape(np.array(accuracy), (test_settings.big_num))))
                    prob = np.reshape(np.array(prob), (test_settings.big_num, test_settings.num_classes))
                    for single_prob in prob:
                        allprob.append(single_prob[1:])
                allprob = np.reshape(np.array(allprob), (-1))
                order = np.argsort(-allprob)

                print('saving all test result...')
                current_step = model_iter
                
                np.save('./out/allprob_iter_' + str(current_step) + '.npy', allprob)
                allans = np.load('chinese_RE/custom_RE/allans.npy', allow_pickle=True)

                # caculate the pr curve area
                average_precision = metrics.average_precision_score(allans, allprob)
                print('PR curve area:' + str(average_precision))


def main(_):

    #If you retrain the model, please remember to change the path to your own model below:
    pathname = "./model_custom/ATT_GRU_model-8800"

    wordembedding = np.load('chinese_RE/custom_RE/vec.npy')
    test_settings = network.Settings()
    test_settings.vocab_size = 16693
    test_settings.num_classes = 16
    test_settings.big_num = 1

    with tf.Graph().as_default():
        sess = tf.Session()
        with sess.as_default():
            def test_step(word_batch, pos1_batch, pos2_batch, y_batch):

                feed_dict = {}
                total_shape = []
                total_num = 0
                total_word = []
                total_pos1 = []
                total_pos2 = []

                for i in range(len(word_batch)):
                    total_shape.append(total_num)
                    total_num += len(word_batch[i])
                    for word in word_batch[i]:
                        total_word.append(word)
                    for pos1 in pos1_batch[i]:
                        total_pos1.append(pos1)
                    for pos2 in pos2_batch[i]:
                        total_pos2.append(pos2)

                total_shape.append(total_num)
                total_shape = np.array(total_shape)
                total_word = np.array(total_word)
                total_pos1 = np.array(total_pos1)
                total_pos2 = np.array(total_pos2)

                feed_dict[mtest.total_shape] = total_shape
                feed_dict[mtest.input_word] = total_word
                feed_dict[mtest.input_pos1] = total_pos1
                feed_dict[mtest.input_pos2] = total_pos2
                feed_dict[mtest.input_y] = y_batch

                loss, accuracy, prob = sess.run(
                    [mtest.loss, mtest.accuracy, mtest.prob], feed_dict)
                return prob, accuracy


            with tf.variable_scope("model"):
                mtest = network.GRU(is_training=False, word_embeddings=wordembedding, settings=test_settings)

            names_to_vars = {v.op.name: v for v in tf.global_variables()}
            saver = tf.train.Saver(names_to_vars)
            saver.restore(sess, pathname)

            print('reading word embedding data...')
            vec = []
            word2id = {}
            f = open('./origin_data/vec.txt', encoding='utf-8')
            content = f.readline()
            content = content.strip().split()
            dim = int(content[1])
            while True:
                content = f.readline()
                if content == '':
                    break
                content = content.strip().split()
                word2id[content[0]] = len(word2id)
                content = content[1:]
                content = [(float)(i) for i in content]
                vec.append(content)
            f.close()
            word2id['UNK'] = len(word2id)
            word2id['BLANK'] = len(word2id)

            print('reading relation to id')
            relation2id = {}
            id2relation = {}
            f = open('chinese_RE/custom_RE/relation2id.txt', 'r', encoding='utf-8')
            while True:
                content = f.readline()
                if content == '':
                    break
                content = content.strip().split()
                relation2id[content[0]] = int(content[1])
                id2relation[int(content[1])] = content[0]

            f.close()

            y_true = []
            y_pred =  []

            with open('chinese_RE/custom_RE/test.txt', encoding='utf-8') as f:
                for orgline in f:
                    line = orgline.strip()
                    # break
                # infile.close()
                    entity1, entity2, rel, sentence = line.split('\t', 3)

                    # print("实体1: " + en1)
                    # print("实体2: " + en2)
                    # print(sentence)
                    # relation = 0
                    en1 = entity1.split('###')[0]
                    en2 = entity2.split('###')[0]
                    en1pos = sentence.find(en1)
                    if en1pos == -1:
                        en1pos = 0
                    en2pos = sentence.find(en2)
                    if en2pos == -1:
                        en2post = 0
                    output = []
                    # length of sentence is 70
                    fixlen = 70
                    # max length of position embedding is 60 (-60~+60)
                    maxlen = 60

                    #Encoding test x
                    for i in range(fixlen):
                        word = word2id['BLANK']
                        rel_e1 = pos_embed(i - en1pos)
                        rel_e2 = pos_embed(i - en2pos)
                        output.append([word, rel_e1, rel_e2])

                    for i in range(min(fixlen, len(sentence))):

                        word = 0
                        if sentence[i] not in word2id:
                            word = word2id['UNK']

                        else:
                            word = word2id[sentence[i]]

                        output[i][0] = word
                    test_x = []
                    test_x.append([output])

                    #Encoding test y
                    label = [0 for i in range(len(relation2id))]
                    label[relation2id[rel]] = 1
                    test_y = []
                    test_y.append(label)

                    test_x = np.array(test_x)
                    test_y = np.array(test_y)

                    test_word = []
                    test_pos1 = []
                    test_pos2 = []

                    for i in range(len(test_x)):
                        word = []
                        pos1 = []
                        pos2 = []
                        for j in test_x[i]:
                            temp_word = []
                            temp_pos1 = []
                            temp_pos2 = []
                            for k in j:
                                temp_word.append(k[0])
                                temp_pos1.append(k[1])
                                temp_pos2.append(k[2])
                            word.append(temp_word)
                            pos1.append(temp_pos1)
                            pos2.append(temp_pos2)

                        test_word.append(word)
                        test_pos1.append(pos1)
                        test_pos2.append(pos2)

                    test_word = np.array(test_word)
                    test_pos1 = np.array(test_pos1)
                    test_pos2 = np.array(test_pos2)

                    prob, accuracy = test_step(test_word, test_pos1, test_pos2, test_y)
                    prob = np.reshape(np.array(prob), (1, test_settings.num_classes))[0]

                    top_id = prob.argsort()[-1]

                    y_true.append(rel)
                    y_pred.append(id2relation[top_id])

                print('准确率:', metrics.accuracy_score(y_true, y_pred))  # 预测准确率输出

                print('宏平均精确率:', metrics.precision_score(y_true, y_pred, average='macro'))  # 预测宏平均精确率输出
                print('微平均精确率:', metrics.precision_score(y_true, y_pred, average='micro'))  # 预测微平均精确率输出
                print('加权平均精确率:', metrics.precision_score(y_true, y_pred, average='weighted'))  # 预测加权平均精确率输出

                print('宏平均召回率:', metrics.recall_score(y_true, y_pred, average='macro'))  # 预测宏平均召回率输出
                print('微平均召回率:', metrics.recall_score(y_true, y_pred, average='micro'))  # 预测微平均召回率输出
                print('加权平均召回率:', metrics.recall_score(y_true, y_pred, average='micro'))  # 预测加权平均召回率输出

                print('宏平均F1-score:',
                      metrics.f1_score(y_true, y_pred, labels=[id2relation[i] for i in list(range(16))], average='macro'))  # 预测宏平均f1-score输出
                print('微平均F1-score:',
                      metrics.f1_score(y_true, y_pred, labels=[id2relation[i] for i in list(range(16))], average='micro'))  # 预测微平均f1-score输出
                print('加权平均F1-score:',
                      metrics.f1_score(y_true, y_pred, labels=[id2relation[i] for i in list(range(16))], average='weighted'))  # 预测加权平均f1-score输出

                # print('混淆矩阵输出:\n', metrics.confusion_matrix(y_true, y_pred, labels=list(range(16))))  # 混淆矩阵输出
                print('分类报告:\n', metrics.classification_report(y_true, y_pred, labels=[id2relation[i] for i in list(range(16))], digits=3))  # 分类报告输出

if __name__ == "__main__":
    tf.app.run()
