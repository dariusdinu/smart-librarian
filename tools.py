book_summaries_dict = {
    "1984": (
        "A dystopian novel by George Orwell. Winston Smith lives in a world where Big Brother watches every move. "
        "He rebels against a regime built on surveillance and propaganda. The story explores freedom, control, and resistance."
    ),
    "The Hobbit": (
        "Bilbo Baggins is thrust into an unexpected journey with a group of dwarves to reclaim treasure from a dragon. "
        "On the way, he discovers bravery, friendship, and hidden strength in a world full of magic and danger."
    ),
    "To Kill a Mockingbird": (
        "A young girl named Scout grows up in the racially charged American South. Her father, Atticus Finch, defends a Black man falsely accused. "
        "The novel explores themes of justice, innocence, and moral growth."
    ),
    "Pride and Prejudice": (
        "Elizabeth Bennet navigates social pressures, misunderstandings, and personal pride. "
        "This classic novel explores love, class, and the challenge of seeing beyond first impressions."
    ),
    "The Catcher in the Rye": (
        "Holden Caulfield, a troubled teen, recounts his journey through New York City after being expelled from school. "
        "He reflects on grief, alienation, and growing up in a world that feels phony."
    ),
    "The Great Gatsby": (
        "Jay Gatsby throws lavish parties hoping to win back Daisy Buchanan. "
        "Set in the 1920s, the novel is a critique of the American Dream, wealth, and illusion."
    ),
    "Brave New World": (
        "In a technologically advanced future, individuality and emotion are suppressed for the sake of societal stability. "
        "The novel explores the cost of conformity and the dangers of state control."
    ),
    "Frankenstein": (
        "Victor Frankenstein creates a living being but is horrified by the result. "
        "The story examines ambition, isolation, and the ethics of scientific discovery."
    ),
    "Harry Potter and the Sorcerer's Stone": (
        "Harry discovers he's a wizard and enters the magical world of Hogwarts. "
        "There, he makes friends, uncovers secrets about his past, and faces an ancient evil. "
        "Themes include friendship, courage, and identity."
    ),
    "The Book Thief": (
        "Narrated by Death, this novel follows Liesel, a girl in Nazi Germany who finds hope through books during horrific times. "
        "Themes include war, resilience, and the power of words."
    )
}

def get_summary_by_title(title: str) -> str:
    return book_summaries_dict.get(title, "No detailed summary available.")
