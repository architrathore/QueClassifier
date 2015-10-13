from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report,confusion_matrix
labels=['DESC', 'ENTY','ABBR','HUM','NUM','LOC']

input=open('data5.txt', 'r')
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
X_train, X_test, y_train, y_test = train_test_split(corpus, corpus_labels, test_size=.3)
# print X_train
# print X_test
# print y_train
# print y_test
X=ngram_vectorizer.fit_transform(X_train).toarray()
X=StandardScaler().fit_transform(X)
testX = ngram_vectorizer.transform(X_test).toarray()
testX=StandardScaler().fit_transform(testX)

print testX

#print(X[0])

#print(type(X))

clf = svm.SVC()
clf.fit(X, y_train) 
#dec = clf.decision_function(X)
#print(dec.shape[1])

lin_clf = svm.LinearSVC()
lin_clf.fit(X, y_train)

intFile.close()
# print "Here"
# print corpus_labels
prediction = []
for i in range(testX.shape[0]):
	# print str(i)+": "+str(clf.predict(X[i])[0])
	prediction.append(clf.predict(testX[i])[0])
print classification_report(prediction,y_test)
	

