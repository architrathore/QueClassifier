from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.gaussian_process import GaussianProcess
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.lda import LDA
from sklearn.qda import QDA
from sklearn.metrics import classification_report,confusion_matrix
from sklearn import cross_validation

labels=['DESC', 'ENTY','HUM','NUM','LOC']

names = [
		 # "Linear SVM", 
		 # "RBF SVM", 
		 # "Poly SVM",
		 # "Sigmoid",
		 # "Decision Tree",
         # "Random Forest", 
         # "AdaBoost", 
         # "Naive Bayes", 
         # "LDA",
         "LogisticRegression",
         # "OneVsRest RBF SVC",
         # "OnevsRest SVC"
         ]

classifiers = [
    # SVC(kernel="linear"),
    # SVC(kernel ="rbf"),
    # SVC(kernel="poly"),
    # SVC(kernel="sigmoid"),
    # DecisionTreeClassifier(max_depth=7),
    # RandomForestClassifier(max_depth=7, n_estimators=10, max_features=1),
    # AdaBoostClassifier(),
    # GaussianNB(),
    # LDA(),
    LogisticRegression(),
    # svm.SVC(),
    # svm.LinearSVC()
	]

input=open('200data', 'r')
intFile = open('intermediate', 'w')
corpus_labels=[]
for line in input:
	flag=0
	a=line.split(':')
	coarse_class=a[0]
	corpus_labels.append(labels.index(coarse_class))
	for i in line:
		if(flag==0):
			if(i==' '):
				flag=1
		else:
			if(i=='?'):
				intFile.write(' ')
			intFile.write(i)

#print(corpus_labels)	

		
corpus=[]
intFile.close()
input.close()
intFile=open('intermediate', 'r')

for line in intFile:
	corpus.append(line[:-1])


ngram_vectorizer = CountVectorizer(ngram_range=(1, 2),token_pattern=r'\b\w+\b', min_df=1)
analyze = ngram_vectorizer.build_analyzer()
pred_list = []
y_test_list = []
for i in xrange(100):
	X_train, X_test, y_train, y_test = train_test_split(corpus, corpus_labels, test_size=.2)
	y_test_list.append(y_test)
	# print X_train
	# print X_test
	# print y_train
	# print y_test
	X_train = ngram_vectorizer.fit_transform(X_train).toarray()
	X_train = StandardScaler().fit_transform(X_train)
	X_test = ngram_vectorizer.transform(X_test).toarray()
	X_test= StandardScaler().fit_transform(X_test)

	for name, clf in zip(names, classifiers):
		# ax = plt.subplot(len(datasets), len(classifiers) + 1, i)
		clf.fit(X_train, y_train)
		# print np.array(y_train).ravel()
		score = clf.score(X_test, y_test)

		prediction = clf.predict(X_test)
		pred_list.append(list(prediction))
		# print "--------------",name,"---------------"
		# print (classification_report(prediction,y_test))
		# print 
		# cm = confusion_matrix(prediction,y_test)
		# print cm
		# print("CORRECT PREDICTIONS:")
		# correct = np.trace(cm)
		# print(correct)
		# print("TOTAL PREDICTIONS:")
		# total = np.sum(cm)
		# print(total)
		# print("ACCURACY:")
		# print(float(correct)/float(total))
		# plt.matshow(cm)
		# plt.title('Confusion matrix for: '+str(name))
		# plt.colorbar()
		# plt.ylabel('True label')
		# plt.xlabel('Predicted label')
a =[item for sublist in pred_list for item in sublist]
b = [item for sublist in y_test_list for item in sublist]
print (classification_report(a,b))
cm = confusion_matrix(a,b)
print "--------------LinearSVC------------"
print cm
print("CORRECT PREDICTIONS:")
correct = np.trace(cm)
print(correct)
print("TOTAL PREDICTIONS:")
total = np.sum(cm)
print(total)
print("ACCURACY:")
print(float(correct)/float(total))
plt.matshow(cm)
plt.title('Confusion matrix for: '+str(name))
plt.colorbar()
plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.show()

# clf = svm.SVC()
# clf.fit(X_train, y_train) 
# #dec = clf.decision_function(X)
# #print(dec.shape[1])

# lin_clf = svm.LinearSVC()
# lin_clf.fit(X_train, y_train)
# prediction = lin_clf.predict(X_test)
# print (classification_report(prediction,y_test))
# print list(prediction)
# print y_test

