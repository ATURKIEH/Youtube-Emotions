#Aref Turkieh
# contains functions that process emotions and comments

EMOTIONS = ['anger', 'joy', 'fear', 'trust', 'sadness', 'anticipation']


def clean_text(comment):
    #this function cleans a comment by replacing non alphabetic characters with spaces and converting the text to lowercase

    return ''.join(c.lower() if c.isalpha() or c.isspace() else ' ' for c in comment)


def make_keyword_dict(keyword_file_name):
    #this function reads a tsv file of keywords and returns a dictionary where
    # each keyword maps to its associated emotions

    keywords = {}
    with open(keyword_file_name, 'r') as file: # reads the file input by the user
        for line in file:
            parts = line.strip().split('\t') # this separates the line with a tab
            word = parts[0]
            emotions = {emotion: int(value) for emotion, value in zip(EMOTIONS, parts[1:])}
            keywords[word] = emotions
    return keywords


def classify_comment_emotion(comment, keywords):
    # this classifies the emotion of a comment using the keyword dictionary

    comment = clean_text(comment)
    emotion_totals = {emotion: 0 for emotion in EMOTIONS}
    words = comment.split()

    for word in words:
        if word in keywords:
            for emotion, value in keywords[word].items():
                emotion_totals[emotion] += value

    # this determines the emotion with the highest score using the priority order in case of ties
    return max(EMOTIONS, key=lambda emotion: (emotion_totals[emotion], -EMOTIONS.index(emotion)))


def make_comments_list(filter_country, comments_file_name):
    # this functions reads a csv file of comments and filters based on the given country

    import csv
    comments = []
    with open(comments_file_name, 'r') as file: #this reads the file input by the user
        reader = csv.reader(file)
        for row in reader:
            comment_id, username, country, text = row
            if filter_country == "all" or country.lower() == filter_country.lower():
                comments.append({ #this adds to the following to the comments
                    'comment_id': int(comment_id),
                    'username': username.strip(),
                    'country': country.strip(),
                    'text': text.strip()
                })
    return comments


def make_report(comment_list, keywords, report_filename):
    #this function generates a report summarizing the emotions in the comments list

    if not comment_list:
        raise RuntimeError("No comments in dataset!")
    #this raises a runtime error after the last comment in the dataset

    emotion_counts = {emotion: 0 for emotion in EMOTIONS}

    for comment in comment_list:
        emotion = classify_comment_emotion(comment['text'], keywords)
        emotion_counts[emotion] += 1
        #increments the emotion counts by 1

    totalComments = sum(emotion_counts.values())
    mostCommonEmotion = max(EMOTIONS, key=lambda emotion: (emotion_counts[emotion], -EMOTIONS.index(emotion)))

    with open(report_filename, 'w') as file:# this writes a file
        file.write(f"Most common emotion: {mostCommonEmotion}\n\n") # display the most common emotions by using the variable name mostCommonEmotion and separating it with a newline
        file.write("Emotion Totals\n") # it writes the total emotions separated by new lines
        for emotion in EMOTIONS:
            percentage = (emotion_counts[emotion] / totalComments * 100) if totalComments else 0
            file.write(f"{emotion}: {emotion_counts[emotion]} ({percentage:.2f}%)\n")
            # this writes the file and rounds up the percentage
    return mostCommonEmotion
