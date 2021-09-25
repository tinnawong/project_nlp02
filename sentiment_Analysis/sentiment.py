from nltk import NaiveBayesClassifier as nbc
from pythainlp.tokenize import word_tokenize
import codecs
from itertools import chain
import os
class sentiment :
	def tran (self):
		#path current
		dirname = os.path.dirname(__file__)

		# pos.txt
		filename_pos = os.path.join(dirname, 'pos.txt')
		with codecs.open(filename_pos, 'r',"utf-8") as f:
			lines = f.readlines()
		listpos=[e.strip() for e in lines]
		del lines
		f.close() # ปิดไฟล์

		# neg.txt
		filename_neg = os.path.join(dirname, '_neg.txt')
		with codecs.open(filename_neg, 'r',"utf-8") as f:
			lines = f.readlines()
		listneg=[e.strip() for e in lines]
		f.close() # ปิดไฟล์

		# ยังไม่ได้ใช้เพราะว่าในส่วน dataset มีน้อยเกินไปทำให้แทรนโมเดลออกมายังไม่ถูกต้องเท่าที่ควรเลยเอาแค่ pos กับ neg
		# with codecs.open('neutral.txt', 'r', "utf-8") as f:
		#     lines = f.readlines()
		# listneu=[e.strip() for e in lines]
		# f.close()

		pos1=['pos']*len(listpos)
		neg1=['neg']*len(listneg)
		training_data = list(zip(listpos,pos1)) + list(zip(listneg,neg1))
		global vocabulary
		global classifier
		vocabulary = set(chain(*[word_tokenize(i[0].lower()) for i in training_data]))
		feature_set = [({i:(i in word_tokenize(sentence.lower())) for i in vocabulary},tag) for sentence, tag in training_data]
		classifier = nbc.train(feature_set)

	def analysis(self,sentence):
		try:
			vocabulary
			# print(vocabulary)
		except Exception as e:
			# print(e)
			self.tran()

		test_sentence = str(sentence)
		featurized_test_sentence = {i: (i in word_tokenize(test_sentence.lower())) for i in vocabulary}
		# print("test_sent:", test_sentence)
		# print("tag:", classifier.classify(featurized_test_sentence))  # ใช้โมเดลที่ train ประมวลผล
		return (test_sentence,classifier.classify(featurized_test_sentence))

if __name__ == '__main__':

	test = sentiment()
	test.tran()

	while(1):
		ss= input("enter :")
		aa = test.analysis(ss)
		print(aa[0],aa[1])

