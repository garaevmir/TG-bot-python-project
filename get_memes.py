def get_meme() :
    arr=[i for i in (1, 24)]
    photo=open(f'memes/mem{random.choice(arr)}.jpg', 'rb')
    return photo