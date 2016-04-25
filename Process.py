import sqlite3
from LinkGetter import LinkGetter
from Parser import Parser

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS `recipes` (
    `name`	TEXT,
    `rules`	TEXT,
    `rules_count`	INTEGER DEFAULT 0,
    `recipe`	TEXT,
    `img`	TEXT,
    `source`	TEXT,
    `id`	INTEGER PRIMARY KEY AUTOINCREMENT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS `ingredients` (
    `name`	TEXT,
    `recipe_id`	INTEGER,
    `id`	INTEGER PRIMARY KEY AUTOINCREMENT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS `records` (
    `key`	TEXT UNIQUE,
    `value`	TEXT
)''')

conn.commit()

while True:
    try:
        cursor.execute("SELECT value FROM records WHERE key = 'page_num'")
        page_num = cursor.fetchone()

        if page_num is None:
            page_num = 1
            insert = True
        else:
            page_num = page_num[0]
            if page_num is None:
                page_num = 1
                insert = True
            else:
                page_num = int(page_num)
                insert = False

        links = LinkGetter.get_links(page_num)

        if links is None:
            print("All receipts learnt, terminating the process...")
            break

        for link in links:
            d = Parser.get_data(link)

            if d is None:
                print("Failed to parse resource: ", d)
                continue

            rules_count = len(d["rules"])
            cursor.execute("INSERT INTO recipes (name, rules, rules_count, recipe, `img`, source) VALUES (?, ?, ?, ?, ?, ?)", (
                d["title"],
                "\n\n".join(d["rules"]),
                rules_count,
                d["recipe"],
                d["image"],
                d["source"]
            ))
            conn.commit()
            recipe_id = cursor.lastrowid

            for i in range(len(d["ingredients"])):
                cursor.execute("INSERT INTO ingredients (name, recipe_id) VALUES (?, ?)", (
                    d["ingredients"][i],
                    recipe_id
                ))
            print("Success parsing resource: ", link)

        if not insert:
            cursor.execute("UPDATE records SET value = '{}' WHERE key = 'page_num'".format(page_num + 1))
        else:
            cursor.execute("INSERT INTO records (key, value) VALUES ('page_num', '{}')".format(page_num + 1))

        conn.commit()
    except Exception as e:
        print("Failure: ", str(e))
        continue
