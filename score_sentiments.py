import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1' 

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense, Dropout
from keras.preprocessing.text import Tokenizer
# from keras.preprocessing.sequence import pad_sequences
from keras_preprocessing.sequence import pad_sequences

# TBD: Generate data from StockTwits
data = {
    'Message': ['Stocks are rising today!', 'Market is going down.', 'Bullish on tech stocks.', 'Earnings report looks good.'],
    'Sentiment': [1, -1, 1, 1]  # 1 for positive, -1 for negative
}

df = pd.DataFrame(data)

# Tokenize and pad sequences
tokenizer = Tokenizer()
tokenizer.fit_on_texts(df['Message'])
X_seq = tokenizer.texts_to_sequences(df['Message'])
X_pad = pad_sequences(X_seq, maxlen=10, padding='post')

# Convert sentiment to numpy array
y = np.array(df['Sentiment'])

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_pad, y, test_size=0.2, random_state=42)

# Build LSTM model
model = Sequential()
model.add(Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=32, input_length=10))
model.add(LSTM(100))
model.add(Dropout(0.2))
model.add(Dense(1, activation='sigmoid'))

# Compile the model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=2, validation_data=(X_test, y_test))

# Evaluate the model on the test set
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {accuracy}")

# Predict sentiments for new data
new_messages = ['Stocks are going up!', 'Market is unpredictable.']
new_seq = tokenizer.texts_to_sequences(new_messages)
new_pad = pad_sequences(new_seq, maxlen=10, padding='post')

predictions = model.predict(new_pad)
predicted_sentiments = [1 if pred > 0.5 else -1 for pred in predictions]

print("Predicted Sentiments:", predicted_sentiments)