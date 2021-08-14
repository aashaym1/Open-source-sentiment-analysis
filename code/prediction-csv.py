from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences


import nltk
nltk.download('punkt')
tokenizer = Tokenizer()


# Max input length (max number of words) 
max_seq_len = 500

for index, row in df.iterrows():
    seq = tokenizer.texts_to_sequences([row['body']])
    padded = pad_sequences(seq, maxlen=max_seq_len)
    pred = model.predict(padded)
    print(row['body'])
    class_result = class_names[np.argmax(pred)]
    data.at[index, "class"] = class_result
    print(class_result)
    