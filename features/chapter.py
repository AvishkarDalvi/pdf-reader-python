from utils.db_utility import connect_database, fetch_questions_by_chapter, close_database

def chapter(chapter_name: str) -> None:
    """Extracts questions from a chapter in the database and prints them to the console.

    Args:
        chapter_name (str): The name of the chapter to extract questions from.

    Returns:
        None
    """
    connection = connect_database()
    questions = fetch_questions_by_chapter(chapter_name, connection)

    if not questions:
        print(f"No questions found for chapter '{chapter_name}'.")
        close_database(connection)
        return

    for question in questions:
        print(f"Subject: {question['subject']}")
        print(f"Chapter: {question['chapter']}")
        print(f"Question: {question['question']}")
        print("Options:")
        for i, option in enumerate([question['option_a'], question['option_b'], question['option_c'], question['option_d']], start=1):
            print(f"  {i}. {option}")
        print(f"Answer: {question['answer']}")
        print("-" * 40)

    close_database(connection)