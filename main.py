class Book:
    def __init__(self, _id, score):
        self._id = _id
        self.score = score

    def __repr__(self):
        return f"Book {self._id}"


class Library:
    def __init__(self, _id, books, signup_time, daily_scans):
        self._id = _id
        self.books = books
        self.signup_time = signup_time
        self.daily_scans = daily_scans
        self.useful_books = dict(books)

    def __repr__(self):
        return f"Library ({self._id}, signup_time: {self.signup_time}, daily_scans: {self.daily_scans})"

    def sort_books(self):
        return [
            str(k)
            for k in sorted(
                self.useful_books.keys(), key=lambda k: -self.useful_books.get(k).score
            )
        ]


def init_problem(input_file):

    with open(input_file) as f:
        input_lines = [[int(e) for e in l.strip("\n").split()] for l in f.readlines()]

    total_time = input_lines[0][2]
    nb_libraries = input_lines[0][1]
    books = dict([(i, Book(i, score)) for i, score in enumerate(input_lines[1])])
    libraries = {}
    for i in range(2, nb_libraries * 2 + 1, 2):
        new_lib = Library(
            _id=int(i / 2) - 1,
            signup_time=input_lines[i][1],
            daily_scans=input_lines[i][2],
            books=dict(
                [(book_id, books.get(book_id)) for book_id in input_lines[i + 1]]
            ),
        )
        libraries[int(i / 2) - 1] = new_lib

    return total_time, libraries, books


def score_submission_file(total_time, libraries, books, submission_file):

    with open(submission_file) as f:
        sub_lines = [[int(e) for e in l.strip("\n").split()] for l in f.readlines()]

    time_gone = 0
    score = 0
    scanned_books = {}
    # Register libraries that signed up before deadline
    for i in range(1, sub_lines[0][0] * 2, 2):
        # Add library signup time to the time spent since the beginning
        time_gone += libraries[sub_lines[i][0]].signup_time
        if time_gone < total_time:
            current_lib = libraries[sub_lines[i][0]]
            # compute the maximum number of books that can actually be signed up
            # based on the remaining time and the library daily scans
            max_number_of_books_scanned = min(
                sub_lines[i][1], (total_time - time_gone) * current_lib.daily_scans
            )
            candidate_books = [
                books.get(j) for j in sub_lines[i + 1][0:max_number_of_books_scanned]
            ]
            # only consider books that were not already scanned
            for b in candidate_books:
                if b._id in scanned_books:
                    pass
                else:
                    scanned_books[b._id] = b
                    score += b.score

        else:
            break

    return score


def generate_result(total_time, libraries, books):
    # Sort libraries by signup time
    sorted_libraries = sort_libraries(libraries, total_time)
    res = [[str(len(sorted_libraries))]]
    scanned_books = {}
    for lib in sorted_libraries:
        # remove already scanned_books

        books_to_add = lib[1].sort_books()
        # discard books already signed up
        books_to_really_add = [b for b in books_to_add if b not in scanned_books]
        if books_to_really_add:
            res.append([str(lib[0]), str(len(books_to_really_add))])
            res.append(books_to_really_add)
            for b in books_to_really_add:
                scanned_books[b] = b
        else:
            res[0][0] = str(int(res[0][0]) - 1)
    return res


def sort_libraries(libraries, total_time):
    key = (
        lambda x: -sum([b.score for i, b in x[1].useful_books.items()])
        / x[1].signup_time
    )

    return sorted(libraries.items(), key=key)


def write_result_to_file(res, output_file):

    # turn res to string
    writable_res = "\n".join([" ".join(l) for l in res])
    with open(output_file, "w+") as f:
        f.write(writable_res)


if __name__ == "__main__":

    input_files = [
        "a_example",
        "b_read_on",
        "c_incunabula",
        "d_tough_choices",
        "e_so_many_books",
        "f_libraries_of_the_world",
    ]

    for file in input_files:
        tot_time, libraries, books = init_problem(f"./input/{file}.txt")
        res = generate_result(tot_time, libraries, books)
        write_result_to_file(res, f"./output/{file}.txt")
        print(score_submission_file(tot_time, libraries, books, f"./output/{file}.txt"))
