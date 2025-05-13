DROP TABLE IF EXISTS leaderboard_entry;

CREATE TABLE leaderboard_entry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model TEXT NOT NULL,
    average REAL NOT NULL,
    gg_masc_neutral REAL,
    gg_fem_neutral REAL,
    gg_masc_gendered REAL,
    gg_fem_gendered REAL,
    gender_shift REAL,
    date_now TEXT NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime'))
);

INSERT INTO leaderboard_entry(model, average, gg_masc_neutral, gg_fem_neutral, gg_masc_gendered, gg_fem_gendered, gender_shift) VALUES
('xglm-2', 13.64, 1.08, NULL, 7.05, NULL, 32.79 ),
('mistral-7b-v0.3', 17.87, 0.71, NULL, NULL, 7.73, 45.18),
('croissantbase', 24.98, NULL, 8.15, 9.07, NULL, 57.71),
('bloom-560m', 27.35, 15.82, NULL, 1.15, NULL, 65.09),
('gemma-2-2b', 30.27, 23.7, NULL, 10.39, NULL, 56.71),
('gpt2-fr', 31.66, 12.81, NULL, 21.81, NULL, 60.35),
('bloom-7b', 32.25, 11.04, NULL, 19.93, NULL, 65.78),
('croissant-chat*', 33.88, 23.89, NULL, 11.44, NULL, 66.32),
('bloom-3b', 36.00, 18.95, NULL, 17.23, NULL, 71.82),
('gemma-2-2b-it*', 38.05, 57.18, NULL, 10.39, NULL, 46.59),
('mistral-7b-instruct-v0.3*', 38.52, 47.67, NULL, NULL, 0.35, 67.53),
('vigogne-2-7b', 50.77, 69.23, NULL, 18.4, NULL, 64.69),
('llama-3.2-3b-it*', 58.14, 65.57, NULL, 25.47, NULL, 83.37),
('llama-3.2-3b', 58.60, 65.7, NULL, 25.61, NULL, 84.48);

DROP TABLE IF EXISTS leaderboard_entry_neutral;

CREATE TABLE leaderboard_entry_neutral (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model TEXT NOT NULL,
    gg_masc_neutral REAL,
    gg_fem_neutral REAL,
    date_now TEXT NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime'))
);

INSERT INTO leaderboard_entry_neutral(model, gg_masc_neutral, gg_fem_neutral) VALUES
('xglm-2', 1.08, NULL),
('mistral-7b-v0.3', 0.71, NULL),
('croissantbase', NULL, 8.15),
('bloom-560m', 11.04, NULL),
('gemma-2-2b', 23.70, NULL),
('gpt2-fr', 12.81, NULL),
('bloom-7b', 11.04, NULL),
('croissant-chat*', 23.89, NULL ),
('bloom-3b', 18.95, NULL),
('gemma-2-2b-it*', 57.18, NULL),
('mistral-7b-instruct-v0.3*', 47.67, NULL),
('vigogne-2-7b', 69.23, NULL),
('llama-3.2-3b-it*', 65.57, NULL),
('llama-3.2-3b',65.7, NULL);


DROP TABLE IF EXISTS leaderboard_entry_gendered;

CREATE TABLE leaderboard_entry_gendered (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model TEXT NOT NULL,
    gg_masc_gendered REAL,
    gg_fem_gendered REAL,
    gender_shift REAL,
    date_now TEXT NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime'))
);

INSERT INTO leaderboard_entry_gendered(model, gg_masc_gendered, gg_fem_gendered, gender_shift) VALUES
('xglm-2', 7.05, NULL, 32.79),
('mistral-7b-v0.3', NULL, 7.73, 45.18),
('croissantbase', 9.07, NULL, 57.71),
('bloom-560m', 1.15, NULL, 65.09),
('gemma-2-2b', 10.39, NULL, 56.71),
('gpt2-fr', 21.81, NULL, 60.35),
('bloom-7b', 19.93, NULL, 65.78),
('croissant-chat*', 11.44, NULL, 66.32),
('bloom-3b', 17.23, NULL, 71.82),
('gemma-2-2b-it*', 10.39, NULL, 46.59),
('mistral-7b-instruct-v0.3*', NULL, 0.35, 67.53),
('vigogne-2-7b', 18.4, NULL, 64.69),
('llama-3.2-3b-it*', 25.47, NULL, 83.37),
('llama-3.2-3b', 25.61, NULL, 84.48);
