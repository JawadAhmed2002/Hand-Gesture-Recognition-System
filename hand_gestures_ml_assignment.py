# -*- coding: utf-8 -*-
"""Hand Gestures ML Assignment.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17ly9RGNGoCUdy11gV25qkmx6iWgkTvKx
"""

# Downloading The Dataset From my Cloud
!gdown 1CJFyiYDeWOXnCQKiere4pYJ7eedOILE7

"""**ML Hand Gesture Recognition Assignmnet.** \
- **In This Jupyter Notebook I Will Implement Different ML Classifier For Hand Gesture Recognition And Will Notedown Its Result and Will Compare Those Results In The Document.**
"""

# Import the necessary libraries or standard libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

"""#**Load Dataset**

**Load the data from the csv file which contains label information at 0th column and remaining columns shows the pixel value at each 784 locations.**
"""

# Read Data with pandas
df = pd.read_csv('sign_mnist.csv')

# Print first 5 rows of dataset using head
df.head()

df.info()

df.shape

df.isnull().sum().sum()

"""## **1. CNN Model For Hand Gesture Sign Language Recognition**
---
"""

# Commented out IPython magic to ensure Python compatibility.
# Google Colab offered several helpful python packages to load in, Import all the Required Libraries For CNN
# %matplotlib inline
import matplotlib.pyplot as plt
from keras.utils.np_utils import to_categorical
from keras import backend as K
from keras.layers import Dense, Dropout,Flatten
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.models import Sequential
from keras.layers import Dropout
from keras.layers.core import Activation

"""**1. In order to feed the model first I have obtained the training data from dataset and load the labels.**\
**2. Use to_categorical to convert the labels into one-hot encoding.**
"""

# Select The Response and Predictor Variables
train=df.drop(['label'], axis = 1) # Features
train = train.values
labels = df['label'] # Labels
labels = to_categorical(labels)
# Take a sample and plot it
sample = train[40]
# Reshape the array as 28 by 28 because the array size is 784
plt.imshow(sample.reshape((28,28)),cmap = plt.get_cmap('gray'))

# get some random index from the train data
random_index = np.random.choice(range(len(train)),12)
# show the 12 random images 
plt.figure(figsize=(10,10))
plt.title("Some Random Training Images")
for i in range(8):
    plt.subplot(3,4,i+1)
    plt.imshow(train[random_index[i]].reshape(28,28),cmap=plt.get_cmap("gray"))
    plt.axis("off")
plt.tight_layout()
plt.show()

"""**Prepare Training and Testing Dataset**"""

print(train.shape,labels.shape)

# Normalize the dataset
train=train/255
train=train.reshape((10000,28,28,1))
plt.imshow(train[40].reshape((28,28)))
print(train.shape,labels.shape)

"""**Below Is The Neural Network Model:** \
* I make use of Convolutional Neural Network(CNN) as my first classifier. Initial 
layer requires the input shape for each row of our training data which is of the shape (28,28,1) and final layer outputs a 25 dimension output.
"""

epochs = 10
batch_size = 32

# Here is the building and training of CNN
model = Sequential()
model.add(Conv2D(filters = 32,kernel_size = (3,3),input_shape = (28,28,1),activation = 'relu',padding = 'same'))
model.add(MaxPooling2D((2,2)))
model.add(Conv2D(filters = 64,kernel_size = (3,3),padding = 'same',activation = 'relu'))
model.add(MaxPooling2D(2,2))
model.add(Conv2D(64,kernel_size = (3,3),padding = 'same',activation = 'relu'))
model.add(Flatten())
model.add(Dense(64,activation = 'relu'))
model.add(Dense(25,activation = 'softmax'))
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
cnn_classifier=model.fit(train, labels, validation_split=0.3, epochs=epochs,batch_size=batch_size)

#Plot the model accuracy and the loss
plt.plot(cnn_classifier.history['accuracy'])
plt.plot(cnn_classifier.history['val_accuracy'])
plt.title('Model accuracy')
plt.show()

plt.plot(cnn_classifier.history['loss'])
plt.plot(cnn_classifier.history['val_loss'])
plt.title('Model Loss')
plt.show()

"""**Testing**
* For testing I first take a sample from the traning data which in our case is from 4th location which has a label 13 and then need to prepare the data to make it suitable for our model to predict.
"""

labels_letter = {0:'A',1:'B',2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H',8:'I',9:'J',10:'K', 11:'L', 12:'M',13:'N',
                 14:'O',15:'P',16:'Q',17:'R',18:'S',19:'T',20:'U',21:'V',22:'W',23:'X',24:'Y',25:'Z'}

sample = train[20]
plt.imshow(sample.reshape((28,28)))
letter_index=labels[20]
print(f'Actual Label Index Of Sample Image Is:{list(letter_index).index(1)}')
print(f'English Letter Of Sample Image Is: {labels_letter[list(letter_index).index(1)]}')

"""* Convert the given image to (1,28,28,1) shape ,normalize it and give it to the model. Find the index of the largest probablitiy from the given set of predictions."""

sample=sample.reshape((1,28,28,1))
res=model.predict(sample)
res=list(res[0])
mx=max(res)
print(f'Predicted Label Index Of Sample Image Is:{res.index(mx)}')
print(f'Predicted English Letter Of Sample Image Is: {labels_letter[res.index(mx)]}')



"""## **2. Random Forest Classifier For Hand Gesture Sign Language Recognition**
---
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
import cv2
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Select The Response and Predictor Variables
predictors=df.values[0:,1:]
response = df.values[0:,0]
# Take a sample and plot it
sample = predictors[25]
# Reshape the array as 28 by 28 because the array size is 784
plt.imshow(sample.reshape((28,28)),cmap=plt.get_cmap("gray"))

# Split the given dataset into training and testing
X = df.iloc[:,1:]
Y = df[['label']]
X_train, X_test, y_train, y_test = train_test_split(X,Y,test_size=0.3,random_state=42)

# Now Train the Model
RFC=RandomForestClassifier(n_estimators=100)
RFC.fit(X_train,y_train)

# finding the score of model
X = df.iloc[:,1:]
Y = df.iloc[:,0]
RFC.score(X_test,y_test)

# Predict the independent variables
res=RFC.predict(X)
res

# Finding out the incorrectly identified labels
total_correct_labels = np.sum(np.squeeze(Y) == res)
print(f'Total Incorrect labels are: {len(df) - total_correct_labels}')

# Finding out the total accuracy of model
test_acc = total_correct_labels / Y.shape[0]
print(f"Test Accuracy: {test_acc * 100} %")

# Finding out the classification report of model
y_pred = RFC.predict(X_test)
report = classification_report(y_pred, y_test)
print(report)

labels_letter = {0:'A',1:'B',2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H',8:'I',9:'J',10:'K', 11:'L', 12:'M',13:'N',
                 14:'O',15:'P',16:'Q',17:'R',18:'S',19:'T',20:'U',21:'V',22:'W',23:'X',24:'Y',25:'Z'}

Imag_number =1
sample = predictors[Imag_number]
plt.imshow(sample.reshape((28,28)),cmap=plt.get_cmap('gray'))
response = df.values[0:,0]
response = to_categorical(response)
letter_index=response[Imag_number]
print(f'Actual Label Index Of Sample Image Is:{list(letter_index).index(1)}')
print(f'English Letter Of Sample Image Is: {labels_letter[list(letter_index).index(1)]}')

row = sample.reshape(1,-1)
res = RFC.predict(row)
mx=max(res)
print(f'Predicted Label Index Of Sample Image Is:{mx}')
print(f'Predicted English Letter Of Sample Image Is: {labels_letter[(mx)]}')



"""##**3. SVM(Support Vector Machine) Multiclass Classifier For Hand Gesture Sign Language Recognition**
---
"""

# Import The Required Libraries
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix, f1_score, accuracy_score,classification_report
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from keras.utils.np_utils import to_categorical

# Select The Response and Predictor Variables
predictors=df.values[0:,1:]
response = df.values[0:,0]
# Take a sample and plot it
sample = predictors[0]
# Reshape the array as 28 by 28 because the array size is 784
plt.imshow(sample.reshape((28,28)),cmap=plt.get_cmap("gray"))

# Split the given dataset into training and testing
X = df.iloc[:,1:]
Y = df[['label']]
# Select the test size as 30 percent and it will set the train size as 70 percent.
X_train, X_test, y_train, y_test = train_test_split(X,Y,test_size=0.3,random_state=42)

#Standardized with Label Encoder
label_enc = LabelEncoder()
y_train = label_enc.fit_transform(y_train)
y_test = label_enc.fit_transform(y_test)

# Train SVM Classifier by keeping decision function shape as one vs all
SVM_classifier = SVC(decision_function_shape='ovr')
SVM_classifier.fit(X_train, y_train)

y_pred = SVM_classifier.predict(X_test)
y_pred

accuracy = accuracy_score(y_test,y_pred)
accuracy

# check out the f1 score for the SVM
f1 = f1_score(y_test,y_pred,average='micro')
f1

# Check out the confusion matrix
cm = confusion_matrix(y_test,y_pred)
cm

# Classification Report
c_report = classification_report(y_pred, y_test)
print(c_report)

# Following are the labels letter
labels_letter = {0:'A',1:'B',2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H',8:'I',9:'J',10:'K', 11:'L', 12:'M',13:'N',
                 14:'O',15:'P',16:'Q',17:'R',18:'S',19:'T',20:'U',21:'V',22:'W',23:'X',24:'Y',25:'Z'}

# Select an image as a sample and check out its letter and actual index
Imag_number =0
sample = predictors[Imag_number]
plt.imshow(sample.reshape((28,28)),cmap = plt.get_cmap('gray'))
response = df.values[0:,0]
response = to_categorical(response)
letter_index=response[Imag_number]
print(f'Actual Label Index Of Sample Image Is:{list(letter_index).index(1)}')
print(f'English Letter Of Sample Image Is: {labels_letter[list(letter_index).index(1)]}')

# Now Reshape the sample and pass it to the trained model if it give similar to the actual than it is better trained
row = sample.reshape(1,-1)
res = SVM_classifier.predict(row)
mx=max(res)
print(f'Predicted Label Index Of Sample Image Is:{mx}')
print(f'Predicted English Letter Of Sample Image Is: {labels_letter[(mx)]}')

#4 Decision tree Classifier

"""# **#4 Decision tree Classifier**"""

# Import The Required Libraries
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix, f1_score, accuracy_score,classification_report
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from keras.utils.np_utils import to_categorical

# Select The Response and Predictor Variables
predictors=df.values[0:,1:]
response = df.values[0:,0]
# Take a sample and plot it
sample = predictors[0]
# Reshape the array as 28 by 28 because the array size is 784
plt.imshow(sample.reshape((28,28)),cmap=plt.get_cmap("gray"))

# Split the given dataset into training and testing
X = df.iloc[:,1:]
Y = df[['label']]
# Select the test size as 30 percent and it will set the train size as 70 percent.
X_train, X_test, y_train, y_test = train_test_split(X,Y,test_size=0.3,random_state=42)

#Standardized with Label Encoder
label_enc = LabelEncoder()
y_train = label_enc.fit_transform(y_train)
y_test = label_enc.fit_transform(y_test)

dec_tree= DecisionTreeClassifier(max_depth=10)
dec_tree.fit(X_train,y_train)

y_pred = dec_tree.predict(X_test)
y_pred

accuracy = accuracy_score(y_test,y_pred)
accuracy

# check out the f1 score for the SVM
f1 = f1_score(y_test,y_pred,average='micro')
f1

# Check out the confusion matrix
cm = confusion_matrix(y_test,y_pred)
cm

# Classification Report
c_report = classification_report(y_pred, y_test)
print(c_report)

# Following are the labels letter
labels_letter = {0:'A',1:'B',2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H',8:'I',9:'J',10:'K', 11:'L', 12:'M',13:'N',
                 14:'O',15:'P',16:'Q',17:'R',18:'S',19:'T',20:'U',21:'V',22:'W',23:'X',24:'Y',25:'Z'}

# Select an image as a sample and check out its letter and actual index
Imag_number =0
sample = predictors[Imag_number]
plt.imshow(sample.reshape((28,28)),cmap = plt.get_cmap('gray'))
response = df.values[0:,0]
response = to_categorical(response)
letter_index=response[Imag_number]
print(f'Actual Label Index Of Sample Image Is:{list(letter_index).index(1)}')
print(f'English Letter Of Sample Image Is: {labels_letter[list(letter_index).index(1)]}')

# Now Reshape the sample and pass it to the trained model if it give similar to the actual than it is better trained
row = sample.reshape(1,-1)
res = dec_tree.predict(row)
mx=max(res)
print(f'Predicted Label Index Of Sample Image Is:{mx}')
print(f'Predicted English Letter Of Sample Image Is: {labels_letter[(mx)]}')

"""##**Classifier App**
---
"""

print('Following Classifier Trained Successfully On The Sign_Mnist Dataset: \n ')
print('1. Convolution Neural Network \n')
print('2. Random Forest Classifier \n')
print('3. SVM Multiclass Classifier \n')
print('4. Decision Tree Classifier \n')

# Here Is The App of the above Classifiers
def app(labels,input_image):
  print('Enter 1 For CNN \n', 'Enter 2 For Random Forest Classifier \n', 'Enter 3 for the SVM \n','Enter 4 For Decision Tree Classifier The App \n', 'Enter 5 For Exit The App \n')
  user_input = int(input('Enter Number To Select The Classifier For The Prediction Of Given Image: '))
  if user_input == 1:
    sample=input_image.reshape((1,28,28,1))
    res=model.predict(sample)
    res=list(res[0])
    mx=max(res)
    print('Below Result Shows The CNN Classification Of The Given Image: \n')
    print(f'Predicted Label Index Of Sample Image Is:{res.index(mx)}')
    print(f'Predicted English Letter Of Sample Image Is: {labels[res.index(mx)]}')

  elif user_input == 2:
    row = input_image.reshape(1,-1)
    res = RFC.predict(row)
    mx=max(res)
    print('Below Result Shows The Random Forest Classification Of The Given Image: \n')
    print(f'Predicted Label Index Of Sample Image Is:{mx}')
    print(f'Predicted English Letter Of Sample Image Is: {labels[(mx)]}')
  
  elif user_input == 3:
    row = input_image.reshape(1,-1)
    res = SVM_classifier.predict(row)
    mx=max(res)
    print('Below Result Shows The SVM Classification Of The Given Image: \n')
    print(f'Predicted Label Index Of Sample Image Is:{mx}')
    print(f'Predicted English Letter Of Sample Image Is: {labels[(mx)]}')
  elif user_input == 4:
    row = input_image.reshape(1,-1)
    res = dec_tree.predict(row)
    mx=max(res)
    print('Below Result Shows The SVM Classification Of The Given Image: \n')
    print(f'Predicted Label Index Of Sample Image Is:{mx}')
    print(f'Predicted English Letter Of Sample Image Is: {labels[(mx)]}')
  elif user_input == 5:
    print('The App Closed, Thank You For Using It!')
    exit()
  
  else:
    print('Please Enter The Correct Input...')

# Here are the labels of the letter along with indices
labels_letter = {0:'A',1:'B',2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H',8:'I',9:'J',10:'K', 11:'L', 12:'M',13:'N',
                 14:'O',15:'P',16:'Q',17:'R',18:'S',19:'T',20:'U',21:'V',22:'W',23:'X',24:'Y',25:'Z'}

# Select any image From the Dataset or You may input here your own hand gesture
Imag_number =0
sample_image = predictors[Imag_number]
plt.imshow(sample_image.reshape((28,28)),cmap=plt.get_cmap("gray"))
response = df.values[0:,0]
response = to_categorical(response)
letter_index=response[Imag_number]
print(f'Actual Label Index Of Sample Image Is:{list(letter_index).index(1)}')
print(f'English Letter Of Sample Image Is: {labels_letter[list(letter_index).index(1)]}')

# Now Pass the sample image and the labels to the classifier app
app(labels_letter, sample_image)

app(labels_letter, sample_image)

app(labels_letter,sample_image)

app(labels_letter, sample_image)

