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
    annotated BOOLEAN,
    csv_row_count INTEGER,
    date_now TEXT NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime'))
);

INSERT INTO leaderboard_entry(model, average, gg_masc_neutral, gg_fem_neutral, gg_masc_gendered, gg_fem_gendered, gender_shift, annotated, csv_row_count) VALUES
('xglm-2', 13.64, 1.08, NULL, 7.05, NULL, 32.79, false, 8898),
('mistral-7b-v0.3', 17.87, 0.71, NULL, NULL, 7.73, 45.18, false, 7636),
('croissantbase', 24.98, NULL, 8.15, 9.07, NULL, 57.71, false, 8322),
('bloom-560m', 27.35, 15.82, NULL, 1.15, NULL, 65.09, false, 8902),
('llama-3.2-3b', 27.88, 33.05, NULL, 10.05, NULL, 40.54, false, 9422),
('gemma-2-2b', 30.27, 23.70, NULL, 10.39, NULL, 56.71, false, 9786),
('gpt2-fr', 31.66, 12.81, NULL, 21.81, NULL, 60.35, false, 9704),
('bloom-7b', 32.25, 11.04, NULL, 19.93, NULL, 65.78, false, 8322),
('croissant-chat*', 33.88, 23.89, NULL, 11.44, NULL, 66.32, false, 9862),
('bloom-3b', 36.00, 18.95, NULL, 17.23, NULL, 71.82, false, 8792),
('mistral-7b-instruct-v0.3*', 38.52, 47.67, NULL, NULL, NULL, 67.53, false, 9552),
('gemma-2-2b-it*', 44.22, 57.18, NULL, 28.88, NULL, 46.59, false, 9190),
('vigogne-2-7b', 50.77, 69.23, NULL, 18.40, NULL, 64.69, false, 8768),
('llama-3.2-3b-it*', 58.14, 65.57, NULL, 25.47, NULL, 83.37, false, 9934);

DROP TABLE IF EXISTS leaderboard_entry_neutral;

CREATE TABLE leaderboard_entry_neutral (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model TEXT NOT NULL,
    gg_masc_neutral REAL,
    gg_fem_neutral REAL,
    annotated BOOLEAN,
    csv_row_count INTEGER,
    date_now TEXT NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime'))
);

INSERT INTO leaderboard_entry_neutral(model, gg_masc_neutral, gg_fem_neutral, annotated, csv_row_count) VALUES
('xglm-2', 1.08, NULL, false, 4481),
('mistral-7b-v0.3', 0.71, NULL, false, 4426),
('croissantbase', NULL, 8.15, false, 4200),
('bloom-560m', 15.82, NULL, false, 4420),
('llama-3.2-3b', 33.05, NULL, false, 4839),
('gemma-2-2b', 23.70, NULL, false, 4901),
('gpt2-fr', 12.81, NULL, false, 4905),
('bloom-7b', 11.04, NULL, false, 4231),
('croissant-chat*', 23.89, NULL, false, 4898),
('bloom-3b', 18.95, NULL, false, 4968),
('mistral-7b-instruct-v0.3*', 47.67, NULL, false, 4887),
('gemma-2-2b-it*', 57.18, NULL, false, 4853),
('vigogne-2-7b', 69.23, NULL, false, 4778),
('llama-3.2-3b-it*', 65.57, NULL, false, 4966);

DROP TABLE IF EXISTS leaderboard_entry_gendered;

CREATE TABLE leaderboard_entry_gendered (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model TEXT NOT NULL,
    gg_masc_gendered REAL,
    gg_fem_gendered REAL,
    gender_shift REAL,
    annotated BOOLEAN,
    csv_row_count INTEGER,
    date_now TEXT NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime'))
);

INSERT INTO leaderboard_entry_gendered(model, gg_masc_gendered, gg_fem_gendered, gender_shift, annotated, csv_row_count) VALUES
('xglm-2', 7.05, NULL, 32.79, false, 4449),
('mistral-7b-v0.3', NULL, 7.73, 45.18, false, 3818),
('croissantbase', 9.07, NULL, 57.71, false, 4181),
('bloom-560m', 1.15, NULL, 65.09, false, 4451),
('llama-3.2-3b', 10.05, NULL, 40.54, false, 4711),
('gemma-2-2b', 10.39, NULL, 56.71, false, 4893),
('gpt2-fr', 21.81, NULL, 60.35, false, 4852),
('bloom-7b', 19.93, NULL, 65.78, false, 4161),
('croissant-chat*', 11.44, NULL, 66.32, false, 4931),
('bloom-3b', 17.23, NULL, 71.82, false, 4396),
('mistral-7b-instruct-v0.3*', NULL, NULL, 67.53, false, 4776),
('gemma-2-2b-it*', 28.88, NULL, 46.59, false, 4595),
('vigogne-2-7b', 18.40, NULL, 64.69, false, 4384),
('llama-3.2-3b-it*', 25.47, NULL, 83.37, false, 4967);
